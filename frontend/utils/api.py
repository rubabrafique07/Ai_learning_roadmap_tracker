import requests

BASE_URL="http://127.0.0.1:8000"

def register(name,email,password):
    response=requests.post(
        f'{BASE_URL}/auth/register',
        json={
            "name":name,
            "email":email,
            "password":password
        }
        )
    return response
        
       
    
def login(email,password):
    response=requests.post(
        f'{BASE_URL}/auth/login',
        json={
            "email":email,
            "password":password
        }
        )
    return response

def get_category(token):
    headers={"Authorization":f'Bearer {token}'}
    return requests.get(
        f'{BASE_URL}/categories/',
        headers=headers
    )

def create_category(token,name):
    headers={"Authorization":f'Bearer {token}'}
    return requests.post(
        f'{BASE_URL}/categories/',
        headers=headers,
        json={
            "name":name
        }
    )

def update_category(token,name,category_id):
    headers={"Authorization":f'Bearer {token}'}
    return requests.put(
        f'{BASE_URL}/categories/{category_id}',
        headers=headers,
        json={"name":name}
    )

def delete_category(token,category_id):
    headers={"Authorization":f'Bearer {token}'}
    return requests.delete(
        f'{BASE_URL}/categories/{category_id}',
        headers=headers

    )


def get_roadmap(token):
    headers={"Authorization":f'Bearer {token}'}
    return requests.get(f'{BASE_URL}/roadmaps/',headers=headers)

def get_roadmap_by_id(token,roadmap_id):
    headers={"Authorization":f'Bearer {token}'}
    return requests.get(
        f'{BASE_URL}/roadmaps/{roadmap_id}',
        headers=headers
    )


def create_roadmap(token, title, deadline, category_id=None):
    headers = {"Authorization": f'Bearer {token}'}
    return requests.post(
        f'{BASE_URL}/roadmaps/',
        headers=headers,
        json={"title": title, "deadline": str(deadline), "category_id": category_id}
    )

def update_roadmap(token,title,deadline,roadmap_id):
    headers={"Authorization":f'Bearer {token}'}
    return requests.put(
        f'{BASE_URL}/roadmaps/{roadmap_id}',
        headers=headers,
        json={
            "title":title,
            "deadline":str(deadline)
            
        }
    )

def delete_roadmap(token,roadmap_id):
    headers={"Authorization":f'Bearer {token}'}
    return requests.delete(
        f'{BASE_URL}/roadmaps/{roadmap_id}',
        headers=headers
    )

def get_topics(token,roadmap_id):
    headers={"Authorization":f'Bearer {token}'}
    return requests.get(
        f'{BASE_URL}/topics/roadmap/{roadmap_id}',
        headers=headers

    )

def get_topic_by_id(token ,topic_id):
    headers={"Authorization":f'Bearer {token}'}
    return requests.get(
        f'{BASE_URL}/topics/{topic_id}',
        headers=headers
    )

def create_topic(token,title,target_date,status,notes,roadmap_id):
    headers={"Authorization":f'Bearer {token}'}
    return requests.post(
        f'{BASE_URL}/topics/{roadmap_id}',
        headers=headers,
        json={"title":title,"target_date":str(target_date),"status":status,"notes":notes}
    )

def update_topic(token,title,target_date,topic_id,status,notes):
    headers={"Authorization":f'Bearer {token}'}
    return requests.put(
        f'{BASE_URL}/topics/{topic_id}',
        headers=headers,
        json={"title":title,"status":status,"target_date":str(target_date),"notes":notes}
    )

def delete_topic(token,topic_id):
    headers={"Authorization":f'Bearer {token}'}
    return requests.delete(
        f'{BASE_URL}/topics/{topic_id}',
        headers=headers
    )

def get_progress_history(token,roadmap_id,topic_id):
    headers={"Authorization":f'Bearer {token}'}
    return requests.get(
        f'{BASE_URL}/progress-history/{roadmap_id}/{topic_id}',
        headers=headers
    )