import pandas as pd

df=pd.read_html('https://www.paloaltonetworks.com/services/support/end-of-life-announcements/hardware-end-of-life-dates')
print(df[0])