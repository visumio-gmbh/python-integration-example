from datetime import timedelta, datetime

from flask import Flask, render_template, session, request, redirect

from client import VisumAPI

app = Flask(__name__)
app.secret_key = 'secret'


MOCK_RUSSIAN_APPLICATION = {
    "passport_data": {
        "name": "Alex",
        "surname": "Mustermann",
        "sex": "Male",
        "place_of_birth": "Some place",
        "passport_number": "74812828",
        "date_of_birth": "04.05.1991",
        "citizenship_country": "DEU",
        "are_changed_name": "Yes",
        "other_names": ["Michael White", "Lil Test"],
        "date_of_passport_issue": "04.05.1992",
        "date_of_passport_expiry": "04.05.2050",
    },
    "personal_data": {
        "was_born_in_russia": "No",
        "have_relatives_in_russia": "No",
        "had_russian_citizenship": "No",
        "currently_work": "No",
        "email": "test@testmail.test",
        "mobile_phone_number": "+79919191122",
        "present_home_address": {
            "country": "RUS",
            "state": "NSO",
            "postcode": "6001924",
            "city": "Novosibirsk",
            "street": "Tereshkovoi",
            "house": "14",
        },
    },
    "travel_data": {
        "places_of_visit": ["Novosibirsk", "Barnaul"],
        "visa_type": "Tourism",
        "visa_validity": "30",
        "consulate": "Bonn",
        "date_of_entry": (datetime.now() + timedelta(days=3)).date().strftime("%d.%m.%Y"),
        "entries": "Single",
        "medical_insurance_number": "38572828",
        "medical_insurance_company_name": "Test company",
        "did_visit_russia_before": "No",
        "tourist_invite_name": "Invite company name",
        "tourist_invite_address": {
            "country": "RUS",
            "state": "NSO",
            "postcode": "6001924",
            "city": "Novosibirsk",
            "street": "Tereshkovoi",
            "house": "15",
        },
        "tourist_invite_confirm_number": "857283412",
        "tourist_invite_reference_number": "294873",
    },
}


@app.get('/')
def select():
    questionnaires = VisumAPI().get_list()
    return render_template('select.html', questionnaires=questionnaires)


@app.get('/q/<int:q_id>')
def get_q(q_id: int):
    questionnaire = VisumAPI().get_by_id(q_id)
    return render_template('q.html', questionnaire=questionnaire)


@app.get('/form/')
def form():
    access_token = session['access_token']
    return render_template('form.html', access_token=access_token)


@app.post('/create_empty_questionnaire/')
def create_empty_questionnaire():
    document_type = request.form.get('document_type')
    questionnaire_data = VisumAPI().create_empty_questionnaire(document_type)
    print(questionnaire_data)
    session['access_token'] = questionnaire_data['access_token']
    return redirect('/form/')


@app.post('/create_questionnaire/')
def create_questionnaire():
    document_type = request.form.get('document_type')
    questionnaire_data = VisumAPI().create_questionnaire(document_type)
    print(questionnaire_data)
    session['access_token'] = questionnaire_data['access_token']
    return redirect('/form/')


@app.post('/open_questionnaire/')
def open_questionnaire():
    access_token = request.form.get('access_token')
    session['access_token'] = access_token
    return redirect('/form/')


@app.post('/<int:q_id>/generate_document/')
def generate_document(q_id: int):
    VisumAPI().generate_document(q_id)
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'some secret key'
    app.run()
