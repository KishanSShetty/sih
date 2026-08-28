import pandas as pd
import os
import csv
import io

def augment_safe_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir))
    data_path = os.path.join(base_dir, 'data', 'processed', 'train.csv')
    
    # SAFE Data to balance the heavy threat dataset
    # We need the model to learn what "Normal" looks like so it doesn't flag everything.
    safe_csv = """text,urgency,authority,fear,impersonation
"Meeting reminder: improving project timelines. Let's discuss this at 2 PM.",0,0,0,0
"HR Update: The annual potluck is scheduled for next Friday. Please bring a dish!",0,0,0,0
"Your Amazon order #402-392 has shipped. Track your package here.",0,0,0,0
"Weekly Newsletter: Top trends in AI and cybersecurity for 2025.",0,0,0,0
"Project Alpha status update: Phase 1 complete. Moving to Phase 2.",0,0,0,0
"Can you please send me the latest slide deck? Thanks.",0,0,0,0
"Reminder: Office closed next Monday for the holiday.",0,0,0,0
"Subscription confirmation: You have successfully subscribed to our service.",0,0,0,0
"Password reset successful. If this was you, no further action is needed.",0,0,0,0
"LinkedIn: You appeared in 5 searches this week.",0,0,0,0
"Google Calendar: Team Sync starting in 10 minutes.",0,0,0,0
"Invoice #2023 attached for your records. Payment due in 30 days.",0,0,0,0
"IT Support: Your ticket #9923 has been resolved.",0,0,0,0
"Happy Birthday! careful wishing you a great day from the team.",0,0,0,0
"Feedback request: How was your recent support experience?",0,0,0,0
"DocuSign: Please review the attached contract draft when you have a moment.",0,0,0,0
"Slack: New message from Sarah in #general.",0,0,0,0
"Zoom: Meeting recording is now available.",0,0,0,0
"Jira: Issue #442 has been updated.",0,0,0,0
"GitHub: Pull request #33 merged into main.",0,0,0,0
"Flight confirmation: Your trip to New York is confirmed.",0,0,0,0
"Hotel reservation: Check-in details for your upcoming stay.",0,0,0,0
"Restaurant receipt: Thank you for dining with us.",0,0,0,0
"Bank Statement: Your monthly statement is ready to view.",0,0,0,0
"Utility Bill: Your electricity bill is available.",0,0,0,0
"Verification code: 123456 is your verification code. Do not share it.",0,0,0,0
"Welcome to the team! We are excited to have you on board.",0,0,0,0
"Policy Update: Please read our updated privacy policy.",0,0,0,0
"System Maintenance: Scheduled downtime this Saturday from 2am to 4am.",0,0,0,0
"Courier update: Your package has been delivered to the front desk.",0,0,0,0
"Team Lunch: We are going to the Italian place downstairs.",0,0,0,0
"Expense report approved. Reimbursement will be processed shortly.",0,0,0,0
"Client meeting reschedule: Moving to Tuesday at 10 AM.",0,0,0,0
"Code review request: Please check the latest commit.",0,0,0,0
"Server status: All systems operational.",0,0,0,0
"Backup complete: Weekly backup finished successfully.",0,0,0,0
"Wifi credentials: The guest network password has changed.",0,0,0,0
"Office supplies: The new printer paper has arrived.",0,0,0,0
"Internal Memo: new security protocols for visitor badges.",0,0,0,0
"Holiday party invitation: RSVP by Friday.",0,0,0,0
"Gym membership: Your renewal is coming up.",0,0,0,0
"Parking permit: please display this on your dashboard.",0,0,0,0
"Cafeteria menu: Today's specials are taco salad and soup.",0,0,0,0
"Lost and Found: A set of keys was found in the break room.",0,0,0,0
"Quarterly All-Hands: Please join us in the main auditorium.",0,0,0,0
"Software update: A new version is available for download.",0,0,0,0
"Library due date: Your book is due back tomorrow.",0,0,0,0
"Appointment confirmation: See you tomorrow at 3 PM.",0,0,0,0
"Volunteer opportunity: Sign up to help at the local shelter.",0,0,0,0
"Charity drive: We are collecting coats this week.",0,0,0,0
"Weather alert: Heavy rain expected this evening. Drive safely.",0,0,0,0
"Traffic update: Accident on I-405, expect delays.",0,0,0,0
"News Alert: Local sports team wins championship.",0,0,0,0
"Daily Digest: Top stories for you.",0,0,0,0
"Recipe of the day: Chocolate chip cookies.",0,0,0,0
"Weekend plans: Are we still on for hiking?",0,0,0,0
"Family reunion: Save the date for next summer.",0,0,0,0
"School closure: Due to snow, schools are closed today.",0,0,0,0
"Movie tickets: Your booking is confirmed.",0,0,0,0
"Concert presale: Tickets go on sale tomorrow.",0,0,0,0"""

    # We will duplicate the safe data to give it significant weight
    # We want roughly 50% split in an ideal world, or at least enough to create a decision boundary.
    # Current Threat count is ~600.
    # 60 samples * 10 = 600 Safe samples.
    
    new_df = pd.read_csv(io.StringIO(safe_csv))
    new_df['cleaned_text'] = new_df['text']
    
    # Duplicate
    final_df = pd.concat([new_df] * 10, ignore_index=True)
    
    if os.path.exists(data_path):
        existing_df = pd.read_csv(data_path)
        existing_texts = set(existing_df['text'].values)
        
        # Only add if not strictly approximate (exact match filter)
        # But for 'Safe' generic texts, we can just append.
        
        final_df.to_csv(data_path, mode='a', header=False, index=False, quoting=csv.QUOTE_ALL)
        print(f"Added {len(final_df)} SAFE training samples to balance the model.")
    else:
        print("Error: Train.csv not found.")

if __name__ == "__main__":
    augment_safe_data()
