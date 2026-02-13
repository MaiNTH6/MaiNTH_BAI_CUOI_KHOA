from playwright.sync_api import expect

class MenuProfile:
    AVATAR_ICON = "(//img[@class='MuiAvatar-img css-45do71'])[1]"
    PROFILE_MENU = "//li[contains(text(),'Profile')]"
    SETTING_MENU = "//li[normalize-space()='Settings']"
    
    TOAST = ".toast-success"

    def __init__(self, page):
        self.page = page

    def open_profile(self):
        # Chờ toast login biến mất (nếu có)
        toast = self.page.locator(self.TOAST)
        if toast.is_visible():
            toast.wait_for(state="hidden", timeout=5000)

        # Click avatar
        avatar = self.page.locator(self.AVATAR_ICON)
        expect(avatar).to_be_visible()
        avatar.click()

        # Click Profile trong menu
        profile = self.page.locator(self.PROFILE_MENU)
        expect(profile).to_be_visible()
        profile.click()

    def open_setting(self):
        # Chờ toast login biến mất (nếu có)
        toast = self.page.locator(self.TOAST)
        if toast.is_visible():
            toast.wait_for(state="hidden", timeout=5000)

        # Click avatar
        avatar = self.page.locator(self.AVATAR_ICON)
        expect(avatar).to_be_visible()
        avatar.click()

        # Click Setting trong menu
        setting = self.page.locator(self.SETTING_MENU)
        expect(setting).to_be_visible()
        setting.click()