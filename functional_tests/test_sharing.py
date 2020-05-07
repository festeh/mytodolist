from functional_tests.base import FunctionalTest
from functional_tests.list_page import ListPage


def force_quit(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    def test_can_share_list_with_others(self):
        # We have two users
        self.create_pre_authd_session("kabanch@ik.ru")
        kabanchik_browser = self.browser
        self.addCleanup(lambda: force_quit(kabanchik_browser))

        self.create_pre_authd_session("baklanch@ik.ru")
        baklanchik_browser = self.setup_browser()
        self.addCleanup(lambda: force_quit(baklanchik_browser))

        # first user creates a task
        kabanchik_browser.get(self.live_server_url)
        kabanchik_page = ListPage(self).add_task_to_list("Tosi bosi")

        share_box = kabanchik_page.get_share_box()
        self.assertEqual(share_box.get_attribute("placeholder"),
                         "your-friend@example.com")

        # and shares with second
        kabanchik_page.share_task_list_with("baklanch@ik.ru")

        self.browser = baklanchik_browser
        baklanchik_page = ListPage(self).go_to_my_lists_page()
        self.browser.find_element_by_link_text("Tosi bosi").click()

        # thee verifies owner and now adds a task
        self.assertEqual(baklanchik_page.get_list_owner(), "kabanch@ik.ru")
        baklanchik_page.add_task_to_list("Ponyal prinyal")

        self.browser = kabanchik_browser
        self.browser.refresh()
        kabanchik_page.wait_row_table(2, "Ponyal prinyal")


