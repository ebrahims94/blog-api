import requests
from typing import Optional
from posts.serializers import PostSerializer, CommentSerializer

API_URL = 'https://jsonplaceholder.typicode.com'

def fetch_posts() -> dict:
    url = API_URL + '/posts'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Failed to fetch posts from API')


def fetch_post_comments(post_id: int) -> dict:
    url = API_URL + f'/posts/{post_id}/comments'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Failed to fetch post comments from API')


def import_data(limit: Optional[int]) -> any:
    posts = fetch_posts()

    try:
        for idx, post in enumerate(posts):
            # no need for user_id since we have default value for it
            del post['userId']
            post_instance = PostSerializer(data=post)
            if post_instance.is_valid():
                created_post = post_instance.save()
                comments = fetch_post_comments(post_id=created_post.id)
                for comment in comments:
                    # format change to follow app format
                    comment['post_id'] = comment['postId']
                    del comment['postId']
                    comment_instance = CommentSerializer(data=comment)
                    if comment_instance.is_valid():
                        comment_instance.save()
            if limit == idx + 1:
                break
    except Exception as e:
        raise Exception("Something went wrong while importing data: ", e)
