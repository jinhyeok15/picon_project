

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
UPDATED = '수정완료'

# 201
CREATED = '생성완료'

# 400
NOT_EXIST_USER = '존재하지 않는 유저입니다.'
