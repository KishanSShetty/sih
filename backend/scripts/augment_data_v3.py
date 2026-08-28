import pandas as pd
import os
import csv
import io
import sys

def augment_data_v3():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_dir))
    data_path = os.path.join(base_dir, 'data', 'processed', 'train.csv')
    
    # Large dataset provided by user
    raw_csv = """text,urgency,authority,fear,impersonation
Court Authority alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
Managing Director alert: unauthorized access detected. Please verify your identity immediately.,1,1,1,1
Managing Director alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
Court Authority alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
Police Department alert: device has been compromised. Please respond within 24 hours.,1,1,1,1
Meta Business Security alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
Court Authority alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1
RBI alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
Microsoft Security Team alert: data leak detected. Please update your information now.,1,1,1,1
Income Tax Department alert: security breach identified. Please complete verification to avoid consequences.,1,1,1,1
Police Department alert: financial loss may occur. Please update your information now.,1,1,1,1
Meta Business Security alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Bank Compliance Department alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
Apple Support alert: legal action will be initiated. Please respond within 24 hours.,1,1,1,1
Managing Director alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Company CEO alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
RBI alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
Managing Director alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
Apple Support alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
FBI alert: data leak detected. Please update your information now.,1,1,1,1
Income Tax Department alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
Apple Support alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
Microsoft Security Team alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
RBI alert: financial loss may occur. Please update your information now.,1,1,1,1
Court Authority alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
RBI alert: device has been compromised. Please update your information now.,1,1,1,1
Apple Support alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Meta Business Security alert: legal action will be initiated. Please respond within 24 hours.,1,1,1,1
Cyber Crime Cell alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Apple Support alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
Police Department alert: data leak detected. Please update your information now.,1,1,1,1
RBI alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
Court Authority alert: device has been compromised. Please verify your identity immediately.,1,1,1,1
Bank Compliance Department alert: penalties will be applied. Please update your information now.,1,1,1,1
HR Department alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
FBI alert: account will be suspended. Please update your information now.,1,1,1,1
Income Tax Department alert: security breach identified. Please respond within 24 hours.,1,1,1,1
Cyber Crime Cell alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
Cyber Crime Cell alert: legal action will be initiated. Please respond within 24 hours.,1,1,1,1
RBI alert: data leak detected. Please update your information now.,1,1,1,1
Court Authority alert: security breach identified. Please verify your identity immediately.,1,1,1,1
Cyber Crime Cell alert: data leak detected. Please update your information now.,1,1,1,1
Apple Support alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
Income Tax Department alert: penalties will be applied. Please verify your identity immediately.,1,1,1,1
Bank Compliance Department alert: legal action will be initiated. Please respond within 24 hours.,1,1,1,1
Income Tax Department alert: penalties will be applied. Please update your information now.,1,1,1,1
Meta Business Security alert: device has been compromised. Please click the link to confirm details.,1,1,1,1
FBI alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
FBI alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
Company CEO alert: financial loss may occur. Please update your information now.,1,1,1,1
Bank Compliance Department alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
Managing Director alert: security breach identified. Please verify your identity immediately.,1,1,1,1
Cyber Crime Cell alert: data leak detected. Please click the link to confirm details.,1,1,1,1
Bank Compliance Department alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Apple Support alert: penalties will be applied. Please update your information now.,1,1,1,1
RBI alert: legal action will be initiated. Please verify your identity immediately.,1,1,1,1
HR Department alert: security breach identified. Please complete verification to avoid consequences.,1,1,1,1
Cyber Crime Cell alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
Company CEO alert: legal action will be initiated. Please update your information now.,1,1,1,1
HR Department alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
Managing Director alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
Meta Business Security alert: device has been compromised. Please update your information now.,1,1,1,1
Cyber Crime Cell alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
Income Tax Department alert: data leak detected. Please update your information now.,1,1,1,1
Apple Support alert: data leak detected. Please click the link to confirm details.,1,1,1,1
Managing Director alert: legal action will be initiated. Please respond within 24 hours.,1,1,1,1
Police Department alert: penalties will be applied. Please verify your identity immediately.,1,1,1,1
Microsoft Security Team alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
Microsoft Security Team alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
Income Tax Department alert: device has been compromised. Please update your information now.,1,1,1,1
Google Security Team alert: penalties will be applied. Please update your information now.,1,1,1,1
HR Department alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
Google Security Team alert: penalties will be applied. Please verify your identity immediately.,1,1,1,1
Google Security Team alert: device has been compromised. Please complete verification to avoid consequences.,1,1,1,1
Police Department alert: device has been compromised. Please verify your identity immediately.,1,1,1,1
Court Authority alert: financial loss may occur. Please update your information now.,1,1,1,1
FBI alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
Meta Business Security alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
Company CEO alert: data leak detected. Please click the link to confirm details.,1,1,1,1
Apple Support alert: financial loss may occur. Please update your information now.,1,1,1,1
Google Security Team alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
Police Department alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
Court Authority alert: unauthorized access detected. Please update your information now.,1,1,1,1
Court Authority alert: account will be suspended. Please update your information now.,1,1,1,1
Meta Business Security alert: unauthorized access detected. Please click the link to confirm details.,1,1,1,1
Managing Director alert: legal action will be initiated. Please update your information now.,1,1,1,1
Court Authority alert: device has been compromised. Please update your information now.,1,1,1,1
Income Tax Department alert: legal action will be initiated. Please respond within 24 hours.,1,1,1,1
Court Authority alert: security breach identified. Please update your information now.,1,1,1,1
FBI alert: penalties will be applied. Please verify your identity immediately.,1,1,1,1
RBI alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
Apple Support alert: unauthorized access detected. Please verify your identity immediately.,1,1,1,1
Google Security Team alert: security breach identified. Please verify your identity immediately.,1,1,1,1
FBI alert: security breach identified. Please update your information now.,1,1,1,1
Income Tax Department alert: device has been compromised. Please complete verification to avoid consequences.,1,1,1,1
Court Authority alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
FBI alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
HR Department alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
Income Tax Department alert: financial loss may occur. Please update your information now.,1,1,1,1
FBI alert: device has been compromised. Please verify your identity immediately.,1,1,1,1
Managing Director alert: device has been compromised. Please update your information now.,1,1,1,1
Cyber Crime Cell alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Bank Compliance Department alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1
Bank Compliance Department alert: unauthorized access detected. Please click the link to confirm details.,1,1,1,1
RBI alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
FBI alert: data leak detected. Please verify your identity immediately.,1,1,1,1
Apple Support alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
Apple Support alert: legal action will be initiated. Please update your information now.,1,1,1,1
FBI alert: security breach identified. Please respond within 24 hours.,1,1,1,1
Managing Director alert: unauthorized access detected. Please click the link to confirm details.,1,1,1,1
Police Department alert: unauthorized access detected. Please update your information now.,1,1,1,1
Income Tax Department alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
RBI alert: security breach identified. Please click the link to confirm details.,1,1,1,1
Police Department alert: device has been compromised. Please update your information now.,1,1,1,1
Apple Support alert: account will be suspended. Please update your information now.,1,1,1,1
Microsoft Security Team alert: account will be suspended. Please update your information now.,1,1,1,1
Court Authority alert: data leak detected. Please update your information now.,1,1,1,1
Microsoft Security Team alert: unauthorized access detected. Please verify your identity immediately.,1,1,1,1
Police Department alert: legal action will be initiated. Please update your information now.,1,1,1,1
Bank Compliance Department alert: data leak detected. Please update your information now.,1,1,1,1
Cyber Crime Cell alert: data leak detected. Please verify your identity immediately.,1,1,1,1
RBI alert: account will be suspended. Please update your information now.,1,1,1,1
Income Tax Department alert: data leak detected. Please verify your identity immediately.,1,1,1,1
FBI alert: device has been compromised. Please respond within 24 hours.,1,1,1,1
Police Department alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
Meta Business Security alert: device has been compromised. Please complete verification to avoid consequences.,1,1,1,1
Company CEO alert: device has been compromised. Please click the link to confirm details.,1,1,1,1
Income Tax Department alert: security breach identified. Please click the link to confirm details.,1,1,1,1
Income Tax Department alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
FBI alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Google Security Team alert: account will be suspended. Please update your information now.,1,1,1,1
Apple Support alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
Google Security Team alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Apple Support alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1
Meta Business Security alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
Apple Support alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Police Department alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1
RBI alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
Police Department alert: data leak detected. Please click the link to confirm details.,1,1,1,1
RBI alert: legal action will be initiated. Please respond within 24 hours.,1,1,1,1
Income Tax Department alert: security breach identified. Please update your information now.,1,1,1,1
Police Department alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
Cyber Crime Cell alert: security breach identified. Please click the link to confirm details.,1,1,1,1
RBI alert: unauthorized access detected. Please update your information now.,1,1,1,1
Microsoft Security Team alert: penalties will be applied. Please update your information now.,1,1,1,1
Income Tax Department alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Google Security Team alert: device has been compromised. Please click the link to confirm details.,1,1,1,1
Company CEO alert: security breach identified. Please verify your identity immediately.,1,1,1,1
Managing Director alert: device has been compromised. Please verify your identity immediately.,1,1,1,1
HR Department alert: security breach identified. Please click the link to confirm details.,1,1,1,1
Company CEO alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
Microsoft Security Team alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
RBI alert: security breach identified. Please verify your identity immediately.,1,1,1,1
Cyber Crime Cell alert: unauthorized access detected. Please verify your identity immediately.,1,1,1,1
FBI alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
Company CEO alert: data leak detected. Please respond within 24 hours.,1,1,1,1
FBI alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
Income Tax Department alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
Police Department alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
Google Security Team alert: unauthorized access detected. Please complete verification to avoid consequences.,1,1,1,1
FBI alert: legal action will be initiated. Please update your information now.,1,1,1,1
RBI alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
Cyber Crime Cell alert: legal action will be initiated. Please update your information now.,1,1,1,1
FBI alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
HR Department alert: penalties will be applied. Please update your information now.,1,1,1,1
Police Department alert: data leak detected. Please verify your identity immediately.,1,1,1,1
HR Department alert: legal action will be initiated. Please respond within 24 hours.,1,1,1,1
Apple Support alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
Google Security Team alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
Bank Compliance Department alert: legal action will be initiated. Please verify your identity immediately.,1,1,1,1
Managing Director alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
Police Department alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
Apple Support alert: device has been compromised. Please respond within 24 hours.,1,1,1,1
Company CEO alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
Apple Support alert: device has been compromised. Please click the link to confirm details.,1,1,1,1
Apple Support alert: unauthorized access detected. Please complete verification to avoid consequences.,1,1,1,1
Google Security Team alert: legal action will be initiated. Please verify your identity immediately.,1,1,1,1
Company CEO alert: security breach identified. Please update your information now.,1,1,1,1
Court Authority alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
Police Department alert: legal action will be initiated. Please verify your identity immediately.,1,1,1,1
Meta Business Security alert: data leak detected. Please update your information now.,1,1,1,1
Police Department alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
Police Department alert: account will be suspended. Please click the link to confirm details.,1,1,1,0
Police Department alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Company CEO alert: penalties will be applied. Please update your information now.,1,1,1,1
Managing Director alert: device has been compromised. Please respond within 24 hours.,1,1,1,1
Bank Compliance Department alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
Bank Compliance Department alert: penalties will be applied. Please verify your identity immediately.,1,1,1,1
Company CEO alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
Cyber Crime Cell alert: unauthorized access detected. Please update your information now.,1,1,1,1
Microsoft Security Team alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Meta Business Security alert: data leak detected. Please verify your identity immediately.,1,1,1,1
Managing Director alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
Meta Business Security alert: legal action will be initiated. Please update your information now.,1,1,1,1
Meta Business Security alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
Microsoft Security Team alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
Company CEO alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
Google Security Team alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
RBI alert: security breach identified. Please complete verification to avoid consequences.,1,1,1,1
Bank Compliance Department alert: data leak detected. Please click the link to confirm details.,1,1,1,1
Google Security Team alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
RBI alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
Cyber Crime Cell alert: penalties will be applied. Please verify your identity immediately.,1,1,1,1
Police Department alert: security breach identified. Please respond within 24 hours.,1,1,1,1
Google Security Team alert: security breach identified. Please click the link to confirm details.,1,1,1,1
Microsoft Security Team alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Court Authority alert: legal action will be initiated. Please respond within 24 hours.,1,1,1,1
Court Authority alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
Meta Business Security alert: account will be suspended. Please update your information now.,1,1,1,1
Google Security Team alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
Google Security Team alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Cyber Crime Cell alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1
Company CEO alert: device has been compromised. Please complete verification to avoid consequences.,1,1,1,1
Microsoft Security Team alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
HR Department alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
Microsoft Security Team alert: unauthorized access detected. Please complete verification to avoid consequences.,1,1,1,1
FBI alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
Bank Compliance Department alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Meta Business Security alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
Company CEO alert: unauthorized access detected. Please update your information now.,1,1,1,1
HR Department alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Court Authority alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
Managing Director alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
Court Authority alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
Meta Business Security alert: unauthorized access detected. Please verify your identity immediately.,1,1,1,1
Income Tax Department alert: unauthorized access detected. Please update your information now.,1,1,1,1
Google Security Team alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
Police Department alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Police Department alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
Microsoft Security Team alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
FBI alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
FBI alert: data leak detected. Please click the link to confirm details.,1,1,1,1
Managing Director alert: device has been compromised. Please click the link to confirm details.,1,1,1,1
Meta Business Security alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
HR Department alert: account will be suspended. Please update your information now.,1,1,1,1
Bank Compliance Department alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
HR Department alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
Police Department alert: security breach identified. Please click the link to confirm details.,1,1,1,1
Cyber Crime Cell alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
Apple Support alert: device has been compromised. Please update your information now.,1,1,1,1
Company CEO alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
FBI alert: penalties will be applied. Please update your information now.,1,1,1,1
HR Department alert: penalties will be applied. Please verify your identity immediately.,1,1,1,1
Microsoft Security Team alert: financial loss may occur. Please update your information now.,1,1,1,1
Cyber Crime Cell alert: security breach identified. Please verify your identity immediately.,1,1,1,1
Cyber Crime Cell alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
Court Authority alert: data leak detected. Please verify your identity immediately.,1,1,1,1
HR Department alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
Microsoft Security Team alert: legal action will be initiated. Please verify your identity immediately.,1,1,1,1
Police Department alert: security breach identified. Please update your information now.,1,1,1,1
RBI alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1
Income Tax Department alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
RBI alert: device has been compromised. Please respond within 24 hours.,1,1,1,1
Apple Support alert: security breach identified. Please update your information now.,1,1,1,1
Cyber Crime Cell alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
Income Tax Department alert: legal action will be initiated. Please verify your identity immediately.,1,1,1,1
HR Department alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
RBI alert: legal action will be initiated. Please update your information now.,1,1,1,1
Apple Support alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
Bank Compliance Department alert: unauthorized access detected. Please update your information now.,1,1,1,1
RBI alert: unauthorized access detected. Please verify your identity immediately.,1,1,1,1
RBI alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Court Authority alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
Income Tax Department alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1
Google Security Team alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
HR Department alert: legal action will be initiated. Please verify your identity immediately.,1,1,1,1
RBI alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
RBI alert: security breach identified. Please update your information now.,1,1,1,1
Cyber Crime Cell alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
Court Authority alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Income Tax Department alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
Microsoft Security Team alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
Bank Compliance Department alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
HR Department alert: security breach identified. Please respond within 24 hours.,1,1,1,1
FBI alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Company CEO alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
Meta Business Security alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
Court Authority alert: penalties will be applied. Please verify your identity immediately.,1,1,1,1
HR Department alert: unauthorized access detected. Please complete verification to avoid consequences.,1,1,1,1
Police Department alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
Apple Support alert: unauthorized access detected. Please update your information now.,1,1,1,1
Court Authority alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Income Tax Department alert: unauthorized access detected. Please click the link to confirm details.,1,1,1,1
HR Department alert: legal action will be initiated. Please update your information now.,1,1,1,1
HR Department alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Bank Compliance Department alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Income Tax Department alert: device has been compromised. Please verify your identity immediately.,1,1,1,1
Managing Director alert: unauthorized access detected. Please update your information now.,1,1,1,1
RBI alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
Google Security Team alert: legal action will be initiated. Please update your information now.,1,1,1,1
Managing Director alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
Company CEO alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
Managing Director alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
Cyber Crime Cell alert: financial loss may occur. Please update your information now.,1,1,1,1
Google Security Team alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
Google Security Team alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
Apple Support alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
Cyber Crime Cell alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
Police Department alert: unauthorized access detected. Please click the link to confirm details.,1,1,1,1
Apple Support alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
Managing Director alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Managing Director alert: security breach identified. Please update your information now.,1,1,1,1
Court Authority alert: security breach identified. Please click the link to confirm details.,1,1,1,1
FBI alert: unauthorized access detected. Please click the link to confirm details.,1,1,1,1
Income Tax Department alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
Court Authority alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Police Department alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
Google Security Team alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Bank Compliance Department alert: unauthorized access detected. Please complete verification to avoid consequences.,1,1,1,1
Bank Compliance Department alert: security breach identified. Please complete verification to avoid consequences.,1,1,1,1
Cyber Crime Cell alert: account will be suspended. Please update your information now.,1,1,1,1
RBI alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
Police Department alert: security breach identified. Please complete verification to avoid consequences.,1,1,1,1
RBI alert: penalties will be applied. Please update your information now.,1,1,1,1
Income Tax Department alert: device has been compromised. Please respond within 24 hours.,1,1,1,1
HR Department alert: device has been compromised. Please click the link to confirm details.,1,1,1,1
Court Authority alert: data leak detected. Please click the link to confirm details.,1,1,1,1
HR Department alert: financial loss may occur. Please update your information now.,1,1,1,1
RBI alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
Microsoft Security Team alert: device has been compromised. Please verify your identity immediately.,1,1,1,1
Court Authority alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
Bank Compliance Department alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
Managing Director alert: data leak detected. Please verify your identity immediately.,1,1,1,1
Police Department alert: penalties will be applied. Please update your information now.,1,1,1,1
Microsoft Security Team alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
Microsoft Security Team alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Managing Director alert: data leak detected. Please update your information now.,1,1,1,1
Police Department alert: security breach identified. Please verify your identity immediately.,1,1,1,1
Court Authority alert: device has been compromised. Please click the link to confirm details.,1,1,1,1
Income Tax Department alert: legal action will be initiated. Please update your information now.,1,1,1,1
Google Security Team alert: data leak detected. Please verify your identity immediately.,1,1,1,1
FBI alert: financial loss may occur. Please respond within 24 hours.,1,1,1,1
Income Tax Department alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Income Tax Department alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
Google Security Team alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
Google Security Team alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
HR Department alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
Google Security Team alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1
HR Department alert: unauthorized access detected. Please verify your identity immediately.,1,1,1,1
Income Tax Department alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
Google Security Team alert: security breach identified. Please respond within 24 hours.,1,1,1,1
Meta Business Security alert: data leak detected. Please respond within 24 hours.,1,1,1,1
Bank Compliance Department alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
Company CEO alert: device has been compromised. Please respond within 24 hours.,1,1,1,1
Police Department alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
Bank Compliance Department alert: security breach identified. Please verify your identity immediately.,1,1,1,1
Company CEO alert: penalties will be applied. Please verify your identity immediately.,1,1,1,1
Court Authority alert: unauthorized access detected. Please complete verification to avoid consequences.,1,1,1,1
HR Department alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
Court Authority alert: legal action will be initiated. Please update your information now.,1,1,1,1
Managing Director alert: legal action will be initiated. Please click the link to confirm details.,1,1,1,1
Meta Business Security alert: financial loss may occur. Please update your information now.,1,1,1,1
Cyber Crime Cell alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
Microsoft Security Team alert: data leak detected. Please verify your identity immediately.,1,1,1,1
Court Authority alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
Bank Compliance Department alert: legal action will be initiated. Please update your information now.,1,1,1,1
Cyber Crime Cell alert: legal action will be initiated. Please verify your identity immediately.,1,1,1,1
HR Department alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Managing Director alert: device has been compromised. Please complete verification to avoid consequences.,1,1,1,1
HR Department alert: legal action will be initiated. Please complete verification to avoid consequences.,1,1,1,1
Managing Director alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1
Bank Compliance Department alert: unauthorized access detected. Please verify your identity immediately.,1,1,1,1
Microsoft Security Team alert: security breach identified. Please verify your identity immediately.,1,1,1,1
Microsoft Security Team alert: security breach identified. Please update your information now.,1,1,1,1
Company CEO alert: account will be suspended. Please update your information now.,1,1,1,1
Income Tax Department alert: account will be suspended. Please update your information now.,1,1,1,1
Income Tax Department alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
Google Security Team alert: data leak detected. Please click the link to confirm details.,1,1,1,1
HR Department alert: security breach identified. Please verify your identity immediately.,1,1,1,1
Court Authority alert: unauthorized access detected. Please click the link to confirm details.,1,1,1,1
Managing Director alert: financial loss may occur. Please update your information now.,1,1,1,1
Cyber Crime Cell alert: security breach identified. Please respond within 24 hours.,1,1,1,1
Managing Director alert: data leak detected. Please click the link to confirm details.,1,1,1,1
Microsoft Security Team alert: legal action will be initiated. Please respond within 24 hours.,1,1,1,1
Google Security Team alert: security breach identified. Please complete verification to avoid consequences.,1,1,1,1
FBI alert: device has been compromised. Please update your information now.,1,1,1,1
HR Department alert: data leak detected. Please click the link to confirm details.,1,1,1,1
Company CEO alert: unauthorized access detected. Please verify your identity immediately.,1,1,1,1
FBI alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
HR Department alert: data leak detected. Please update your information now.,1,1,1,1
Managing Director alert: security breach identified. Please click the link to confirm details.,1,1,1,1
Court Authority alert: penalties will be applied. Please update your information now.,1,1,1,1
Company CEO alert: device has been compromised. Please verify your identity immediately.,1,1,1,1
Microsoft Security Team alert: unauthorized access detected. Please update your information now.,1,1,1,1
Google Security Team alert: financial loss may occur. Please update your information now.,1,1,1,1
Cyber Crime Cell alert: penalties will be applied. Please complete verification to avoid consequences.,1,1,1,1
Police Department alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Cyber Crime Cell alert: device has been compromised. Please click the link to confirm details.,1,1,1,1
Meta Business Security alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
Apple Support alert: unauthorized access detected. Please click the link to confirm details.,1,1,1,1
RBI alert: device has been compromised. Please verify your identity immediately.,1,1,1,1
RBI alert: security breach identified. Please respond within 24 hours.,1,1,1,1
Meta Business Security alert: unauthorized access detected. Please update your information now.,1,1,1,1
Managing Director alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Company CEO alert: unauthorized access detected. Please click the link to confirm details.,1,1,1,1
Microsoft Security Team alert: device has been compromised. Please click the link to confirm details.,1,1,1,1
FBI alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
Apple Support alert: security breach identified. Please complete verification to avoid consequences.,1,1,1,1
Meta Business Security alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Microsoft Security Team alert: legal action will be initiated. Please update your information now.,1,1,1,1
Company CEO alert: security breach identified. Please respond within 24 hours.,1,1,1,1
Meta Business Security alert: penalties will be applied. Please verify your identity immediately.,1,1,1,1
Cyber Crime Cell alert: unauthorized access detected. Please click the link to confirm details.,1,1,1,1
Bank Compliance Department alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
Police Department alert: device has been compromised. Please complete verification to avoid consequences.,1,1,1,1
HR Department alert: device has been compromised. Please update your information now.,1,1,1,1
HR Department alert: device has been compromised. Please complete verification to avoid consequences.,1,1,1,1
FBI alert: security breach identified. Please complete verification to avoid consequences.,1,1,1,1
Managing Director alert: security breach identified. Please respond within 24 hours.,1,1,1,1
Google Security Team alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
FBI alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1
Bank Compliance Department alert: financial loss may occur. Please click the link to confirm details.,1,1,1,1
Microsoft Security Team alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
Company CEO alert: data leak detected. Please update your information now.,1,1,1,1
Meta Business Security alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1
RBI alert: data leak detected. Please click the link to confirm details.,1,1,1,1
Meta Business Security alert: legal action will be initiated. Please verify your identity immediately.,1,1,1,1
Apple Support alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
Apple Support alert: security breach identified. Please click the link to confirm details.,1,1,1,1
Google Security Team alert: data leak detected. Please update your information now.,1,1,1,1
Microsoft Security Team alert: device has been compromised. Please update your information now.,1,1,1,1
Microsoft Security Team alert: penalties will be applied. Please verify your identity immediately.,1,1,1,1
Managing Director alert: financial loss may occur. Please verify your identity immediately.,1,1,1,1
Apple Support alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Microsoft Security Team alert: device has been compromised. Please complete verification to avoid consequences.,1,1,1,1
Managing Director alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
Cyber Crime Cell alert: financial loss may occur. Please complete verification to avoid consequences.,1,1,1,1
Managing Director alert: security breach identified. Please complete verification to avoid consequences.,1,1,1,1
Bank Compliance Department alert: account will be suspended. Please complete verification to avoid consequences.,1,1,1,1
Court Authority alert: device has been compromised. Please respond within 24 hours.,1,1,1,1
Microsoft Security Team alert: data leak detected. Please click the link to confirm details.,1,1,1,1
Google Security Team alert: unauthorized access detected. Please verify your identity immediately.,1,1,1,1
Court Authority alert: device has been compromised. Please complete verification to avoid consequences.,1,1,1,1
Court Authority alert: security breach identified. Please complete verification to avoid consequences.,1,1,1,1
Bank Compliance Department alert: security breach identified. Please click the link to confirm details.,1,1,1,1
Meta Business Security alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
Police Department alert: unauthorized access detected. Please complete verification to avoid consequences.,1,1,1,1
Cyber Crime Cell alert: device has been compromised. Please respond within 24 hours.,1,1,1,1
Bank Compliance Department alert: device has been compromised. Please update your information now.,1,1,1,1
Microsoft Security Team alert: security breach identified. Please complete verification to avoid consequences.,1,1,1,1
Microsoft Security Team alert: device has been compromised. Please respond within 24 hours.,1,1,1,1
Bank Compliance Department alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
RBI alert: unauthorized access detected. Please respond within 24 hours.,1,1,1,1
Google Security Team alert: unauthorized access detected. Please update your information now.,1,1,1,1
Bank Compliance Department alert: device has been compromised. Please click the link to confirm details.,1,1,1,1
Court Authority alert: security breach identified. Please respond within 24 hours.,1,1,1,1
Company CEO alert: account will be suspended. Please respond within 24 hours.,1,1,1,1
Cyber Crime Cell alert: account will be suspended. Please click the link to confirm details.,1,1,1,1
FBI alert: security breach identified. Please verify your identity immediately.,1,1,1,1
FBI alert: financial loss may occur. Please update your information now.,1,1,1,1
Bank Compliance Department alert: device has been compromised. Please respond within 24 hours.,1,1,1,1
Google Security Team alert: security breach identified. Please update your information now.,1,1,1,1
Court Authority alert: legal action will be initiated. Please verify your identity immediately.,1,1,1,1
Apple Support alert: data leak detected. Please verify your identity immediately.,1,1,1,1
FBI alert: legal action will be initiated. Please verify your identity immediately.,1,1,1,1
Microsoft Security Team alert: account will be suspended. Please verify your identity immediately.,1,1,1,1
Apple Support alert: security breach identified. Please verify your identity immediately.,1,1,1,1
Bank Compliance Department alert: penalties will be applied. Please respond within 24 hours.,1,1,1,1
Microsoft Security Team alert: penalties will be applied. Please click the link to confirm details.,1,1,1,1
FBI alert: unauthorized access detected. Please verify your identity immediately.,1,1,1,1
Cyber Crime Cell alert: device has been compromised. Please update your information now.,1,1,1,1
FBI alert: legal action will be initiated. Please respond within 24 hours.,1,1,1,1
Income Tax Department alert: unauthorized access detected. Please complete verification to avoid consequences.,1,1,1,1
Microsoft Security Team alert: data leak detected. Please complete verification to avoid consequences.,1,1,1,1"""

    # Parse and merge
    new_df = pd.read_csv(io.StringIO(raw_csv))
    new_df['cleaned_text'] = new_df['text']
    
    if os.path.exists(data_path):
        existing_df = pd.read_csv(data_path)
        existing_texts = set(existing_df['text'].values)
        new_df = new_df[~new_df['text'].isin(existing_texts)]
        
        if not new_df.empty:
            new_df.to_csv(data_path, mode='a', header=False, index=False, quoting=csv.QUOTE_ALL)
            print(f"Added {len(new_df)} new training samples.")
        else:
            print("No new unique samples found.")
    else:
        new_df.to_csv(data_path, index=False, quoting=csv.QUOTE_ALL)
        print(f"Created new dataset with {len(new_df)} samples.")

if __name__ == "__main__":
    augment_data_v3()
