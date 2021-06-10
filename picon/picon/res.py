

def response_data(code, msg, **kwargs):
    data = {
        'statusCode': code,
        'responseMessage': msg,
    }
    for key, value in kwargs.items():
        data[key] = value
    return data


# 200
OK = '조회성공'

# 201
CREATED = '생성완료'
UPDATED = '수정완료'

# 400
NOT_EXIST_USER = '존재하지 않는 유저입니다.'
SAME_ID = '본인을 팔로우할 수 없습니다.'
