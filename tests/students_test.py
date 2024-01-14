ASSIGNMENT_ID = None

def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1
        assert assignment['state'] in ['DRAFT', 'SUBMITTED', 'GRADED']



def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2
        assert assignment['state'] in ['DRAFT', 'SUBMITTED', 'GRADED']


    assert len(data) == 6


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_wrong_header_1(client, h_student_3):
    response = client.post(
        '/student/assignments',
        headers=h_student_3
    )

    assert response.status_code == 403



def test_no_header_1(client):
    response = client.post(
        '/student/assignments',
    )

    assert response.status_code == 401


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['id'] is not None
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None
    assert data['grade'] is None

    global ASSIGNMENT_ID 
    ASSIGNMENT_ID = data['id']

def test_post_assignment_edit_student_1(client, h_student_1):
    content = 'Updated content'
    global ASSIGNMENT_ID
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={

            'id': ASSIGNMENT_ID,
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['id'] == ASSIGNMENT_ID
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None
    assert data['grade'] is None


def test_post_assignment_edit_student_2(client, h_student_1):
    content = 'Updated content'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={

            'id': 1,
            'content': content
        })

    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only assignment in draft state can be edited'


def test_wrong_header_2(client, h_student_3):
    content = 'Updated content'

    response = client.post(
        '/student/assignments',
        headers=h_student_3,
        json={

            'id': 1,
            'content': content
        })

    assert response.status_code == 403



def test_no_header_2(client):
    content = 'Updated content'

    response = client.post(
        '/student/assignments',
        json={

            'id': 1,
            'content': content
        })

    assert response.status_code == 401


def test_submit_assignment_student_1(client, h_student_1):

    global ASSIGNMENT_ID
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': ASSIGNMENT_ID,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'


def test_wrong_header_3(client, h_student_3):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_3
    )

    assert response.status_code == 403



def test_no_header_3(client):
    response = client.post(
        '/student/assignments/submit',
    )

    assert response.status_code == 401
