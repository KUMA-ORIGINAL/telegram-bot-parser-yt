import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent


def get_info(url):
    ua = UserAgent(browsers=['chrome'])
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent: {ua.random}')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(10)
    name_video = driver.find_element(By.CSS_SELECTOR, 'h1.style-scope.ytd-watch-metadata').text
    name_channel, subscribers = driver.find_element(By.CLASS_NAME,
                                                    'style-scope ytd-video-owner-renderer').text.split('\n')
    likes = driver.find_element(By.ID, 'segmented-like-button').text
    views = driver.find_element(By.ID, 'info-container').text
    driver.close()

    return url, name_channel, subscribers, name_video, views[0:views.index('просмотров')-1], likes


# class YouTubeChannel:
#     videos = []
#
#     def __init__(self):
#         ua = UserAgent(browsers=['chrome'])
#         options = webdriver.ChromeOptions()
#         options.add_argument(f'user-agent: {ua.random}')
#         self.driver = webdriver.Chrome(options=options)
#
#     def get_name_channel(self, url):
#         self.driver.get(url)
#         time.sleep(3)
#         info = self.driver.find_element(By.CLASS_NAME, 'style-scope ytd-watch-metadata').text.split('\n')
#         return f'Имя канала: {info[1]}'
#
#     def get_number_subscribers(self, url):
#
#         info = self.driver.find_element(By.CLASS_NAME, 'style-scope ytd-watch-metadata').text.split('\n')
#         return f'Количество подписчиков: {info[2][0:8]}'
#
#     def add_video(self, url):
#         if url in YouTubeChannel.videos:
#             return f'Это видео уже в списке'
#         else:
#             YouTubeChannel.videos.append(url)
#
#     def del_video(self, url_video):
#         if url in self.videos:
#             self.videos.remove(url_video)
#         else:
#             print('Этого видео нет в списке')
#
#     def get_videos(self):
#         return self.videos
#
#
# class Videos(YouTubeChannel):
#     def get_name_video(self, url):
#         self.driver.get(url)
#         time.sleep(3)
#         info = self.driver.find_element(By.CLASS_NAME, 'style-scope ytd-watch-metadata').text.split('\n')
#         return f'Название видео: {info[0]}'
#
#     def get_number_views(self, url):
#         self.driver.get(url)
#         time.sleep(3)
#         info = self.driver.find_element(By.CLASS_NAME, 'style-scope ytd-watch-metadata').text.split('\n')
#         return f'Количество просмотров: {info[8][0:8]}'
#
#     def get_number_likes(self, url):
#         self.driver.get(url)
#         time.sleep(3)
#         info = self.driver.find_element(By.CLASS_NAME, 'style-scope ytd-watch-metadata').text.split('\n')
#         return f'Количество лайков: {info[4]}'
#
#
# url = 'https://www.youtube.com/watch?v=kudbejO_K68&t=32s'
# url2 = 'https://www.youtube.com/watch?v=SuvUyO7R4B8&t=1s'
