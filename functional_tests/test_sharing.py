from functional_tests.base import FunctionalTest


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
        self.add_task_to_list("Tosi bosi")

        share_box = self.browser.find_element_by_css_selector(
            'input[name="share"]'
        )
        self.assertEqual(share_box.get_attribute("placeholder"),
                         "your-friend@example.com")



