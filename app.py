import joblib
import streamlit as st # type: ignore
import pandas as pd
import pickle
import plotly.graph_objects as go

teams = ['Sunrisers Hyderabad',
         'Mumbai Indians',
         'Royal Challengers Bangalore',
         'Kolkata Knight Riders',
         'Punjab Kings',
         'Chennai Super Kings',
         'Rajasthan Royals',
         'Delhi Capitals',
         'Lucknow Super Giants',
         'Gujarat Titans']

cities = ['Ahmedabad', 'Mumbai', 'Navi Mumbai', 'Pune', 'Dubai', 'Sharjah',
          'Abu Dhabi', 'Delhi', 'Chennai', 'Hyderabad', 'Visakhapatnam',
          'Chandigarh', 'Bengaluru', 'Kolkata', 'Jaipur', 'Indore',
          'Bangalore', 'Raipur', 'Ranchi', 'Cuttack', 'Dharamsala', 'Nagpur',
          'Johannesburg', 'Centurion', 'Durban', 'Bloemfontein',
          'Port Elizabeth', 'Kimberley', 'East London', 'Cape Town']

pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title('IPL Win Predictor')
st.image("https://i1.wp.com/crickettimes.com/wp-content/uploads/2023/03/IPL-2023-broadcast-and-streaming-details-1260x657.jpg?strip=all")

col1, col2 = st.columns(2)

with col1:
    BattingTeam = st.selectbox('Batting Team', sorted(teams))
with col2:
    BowlingTeam = st.selectbox('Bowling Team', sorted(teams))

selected_city = st.selectbox('Select Venue', sorted(cities))

target = st.number_input('Target')

col3, col4, col5 = st.columns(3)

with col3:  
    score = st.number_input('Score')
with col4:
    overs = st.slider('Overs Completed', 0, 20, 10)
with col5:
    wickets = st.slider('Wickets', 0, 10, 2)


if st.button('Predict'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets = 10 - wickets
    crr = score / overs
    rrr = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({'BattingTeam': [BattingTeam], 'BowlingTeam': [BowlingTeam],
                         'City': [selected_city], 'runs_left': [runs_left], 'balls_left': [balls_left],
                         'wickets_left': [wickets], 'total_run_x': [target], 'crr': [crr], 'rrr': [rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(BattingTeam + "- " + str(round(win * 100)) + "%")
    st.header(BowlingTeam + "- " + str(round(loss * 100)) + "%")

    overs_range = list(range(1, int(overs)+1))
    win_probabilities = []

    for over in overs_range:
        balls_left_dynamic = 120 - (over * 6)
        crr_dynamic = score / over
        rrr_dynamic = (runs_left * 6) / balls_left_dynamic

        input_df_dynamic = pd.DataFrame({'BattingTeam': [BattingTeam], 'BowlingTeam': [BowlingTeam],
                                         'City': [selected_city], 'runs_left': [runs_left], 'balls_left': [balls_left_dynamic],
                                         'wickets_left': [wickets], 'total_run_x': [target], 'crr': [crr_dynamic], 'rrr': [rrr_dynamic]})

        result_dynamic = pipe.predict_proba(input_df_dynamic)
        win_probabilities.append(result_dynamic[0][1] * 100)  # Convert to percentage

    # Plot the win probabilities over time using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=overs_range, y=win_probabilities, mode='lines+markers'))

    fig.update_layout(title='Win Probability Over Time',
                      xaxis_title='Overs',
                      yaxis_title='Win Probability (%)')

    st.plotly_chart(fig)


# #     ID	                   match_id 
# #     innings	
# #     overs	               over 
# #     ballnumber             over
# #     batter	               striker
# #     bowler	               bowler
# #     non-striker	 
# #     extra_type	           extras
# #     batsman_run	           runs_of_bat
# #     extras_run	
# #     total_run	
# #     non_boundary	
# #     isWicketDelivery	   wicket_type
# #     player_out	           player_dismissed
# #     kind	               wicket_type
# #     fielders_involved	   fielder
# #     BattingTeam            batting_team


# # season (Year)
# # match_no (Match No. in a season)
# # date (Match Date)
# # venue (Stadium name and Location)
# # batting_team (Team Name)
# # bowling_team (Team Name)
# # innings (1,2)
# # runs_of_bat (Runs scored by Striker)
# # extras (Runs in Extras)
# # wide (1,0)
# # legbyes (1,0)
# # byes (1,0)
# # noballs (1,0)
# # player_dismissed (Player Name)
# # wicket_type ('Caught', 'Stumped', 'Bowled', 'Run out', 'LBW', 'Retired out', 'Retired hurt', 'obstructing the field')
# # fielder

# import streamlit as st
# import pandas as pd
# import pickle
# import smtplib
# from email.mime.text import MIMEText

# # Load the trained model
# pipe = pickle.load(open('pipe.pkl', 'rb'))

# # Teams and venues
# teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
#          'Kolkata Knight Riders', 'Punjab Kings', 'Chennai Super Kings',
#          'Rajasthan Royals', 'Delhi Capitals', 'Lucknow Super Giants', 'Gujarat Titans']

# cities = ['Ahmedabad', 'Mumbai', 'Navi Mumbai', 'Pune', 'Dubai', 'Sharjah',
#           'Abu Dhabi', 'Delhi', 'Chennai', 'Hyderabad', 'Visakhapatnam',
#           'Chandigarh', 'Bengaluru', 'Kolkata', 'Jaipur', 'Indore',
#           'Bangalore', 'Raipur', 'Ranchi', 'Cuttack', 'Dharamsala', 'Nagpur',
#           'Johannesburg', 'Centurion', 'Durban', 'Bloemfontein',
#           'Port Elizabeth', 'Kimberley', 'East London', 'Cape Town']

# # Title and image
# st.title('IPL Win Predictor')
# st.image("https://i1.wp.com/crickettimes.com/wp-content/uploads/2023/03/IPL-2023-broadcast-and-streaming-details-1260x657.jpg?strip=all")

# # Input columns
# col1, col2 = st.columns(2)

# with col1:
#     BattingTeam = st.selectbox('Batting Team', sorted(teams))
# with col2:
#     BowlingTeam = st.selectbox('Bowling Team', sorted(teams))

# selected_city = st.selectbox('Select Venue', sorted(cities))
# target = st.number_input('Target')

# col3, col4, col5 = st.columns(3)

# with col3:  
#     score = st.number_input('Score')
# with col4:
#     overs = st.number_input('Overs Completed')
# with col5:
#     wickets = st.number_input('Wickets')

# # Email alert setup
# def send_alert(email, message):
#     msg = MIMEText(message)
#     msg['Subject'] = 'IPL Win Predictor Alert'
#     msg['From'] = 'kattimanijai@gmail.com'
#     msg['To'] = email

#     try:
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.starttls()  # Upgrade the connection to TLS
#             server.login('kattimanijai@gmail.com', 'gmail2000@1145')
#             server.sendmail('kattimanijai@gmail.com', email, msg.as_string())
#             st.success("Email alert sent successfully!")
#     except Exception as e:
#         st.error(f"Failed to send email: {e}")

# # Prediction button
# if st.button('Predict'):
#     runs_left = target - score
#     balls_left = 120 - (overs * 6)
#     wickets = 10 - wickets
#     crr = score / overs
#     rrr = (runs_left * 6) / balls_left

#     input_df = pd.DataFrame({
#         'BattingTeam': [BattingTeam], 
#         'BowlingTeam': [BowlingTeam],
#         'City': [selected_city], 
#         'runs_left': [runs_left], 
#         'balls_left': [balls_left],
#         'wickets_left': [wickets], 
#         'total_run_x': [target], 
#         'crr': [crr], 
#         'rrr': [rrr]
#     })

#     result = pipe.predict_proba(input_df)
#     loss = result[0][0]
#     win = result[0][1]
    
#     st.header(f"{BattingTeam} - {round(win * 100)}%")
#     st.header(f"{BowlingTeam} - {round(loss * 100)}%")

#     # Send email alert if win probability is high
#     if win > 0.7:
#         user_email = st.text_input("Enter your email to receive an alert:")
#         if user_email:
#             send_alert(user_email, f"{BattingTeam} has a high chance of winning ({round(win * 100)}%) against {BowlingTeam}!")

