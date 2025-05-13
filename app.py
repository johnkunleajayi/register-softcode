from flask import Flask, render_template, request, flash, redirect, url_for
from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')  # required for flashing messages

# Salesforce authentication
def authenticate_salesforce():
    try:
        sf = Salesforce(
            username=os.getenv("SALESFORCE_USERNAME"),
            password=os.getenv("SALESFORCE_PASSWORD"),
            security_token=os.getenv("SALESFORCE_SECURITY_TOKEN")
        )
        print("✅ Connected to Salesforce")
        return sf
    except Exception as e:
        print(f"❌ Salesforce auth error: {e}")
        return None

# Home route: Signup page (GET + POST)
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        try:
            sf = authenticate_salesforce()
            if not sf:
                raise Exception("Could not connect to Salesforce.")
            
            result = sf.Prospective_Student__c.create({
    'First_Name__c': data.get('fname'),
    'Last_Name__c': data.get('lname'),
    'Email__c': data.get('email'),
    'Phone_Number__c': data.get('phone_number'),
    'Location_Country__c': data.get('location'),
    'How_did_you_hear_about_us_Select_one__c': data.get('hear'),
    'Training_Plan__c': data.get('plan'),
    'What_is_your_current_role__c': data.get('current'),
    'How_would_you_rate_your_Salesforce_dev__c': data.get('sfdev'),
    'How_would_you_rate_your_Python_dev__c': data.get('pythondev'),
    'What_are_your_main_goals_for_attending__c': data.get('goals'),
    'Do_you_have_any_specific_questions_or__c': data.get('specific'),
    'Would_you_like_updates_about_SoftCode__c': bool(data.get('updates')),
    'Are_you_committed_to_4_hrs_each_weekend__c': bool(data.get('weekend')),
    'Are_you_commited_to_4_hrs_self_practice__c': bool(data.get('practice')),
    'Comments__c': data.get('comments'),
})


            flash("You have successfully signed up. You will get a mail from us soon!", "success")
            return redirect(url_for('signup'))

        except Exception as e:
            flash(f"❌ Signup failed: {str(e)}", "error")
            return redirect(url_for('signup'))

    return render_template('signup.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
