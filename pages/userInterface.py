
import streamlit as st

st.title("User Interface")
st.text("Name:")
firstName = st.text_input("First")
lastName = st.text_input("Last")
st.text("Birthday:")
birthday = st.date_input("Your Birthday")
st.text("Address:")
street = st.text_input("Street")
city = st.text_input("City")
state = option = st.selectbox(
   "State:",
   ("Alabama",
"Alaska"
,"Arizona"
,"Arkansas"
,"California"
,"Colorado"
,"Connecticut"
,"Delaware"
,"Florida"
,"Georgia"
,"Hawaii"
,"Idaho"
,"Illinois"
,"Indiana"
,"Iowa"
,"Kansas"
,"Kentucky"
,"Louisiana"
,"Maine"
,"Maryland"
,"Massachusetts"
,"Michigan"
,"Minnesota"
,"Mississippi"
,"Missouri"
,"Montana"
,"Nebraska"
,"Nevada"
,"New Hampshire"
,"New Jersey"
,"New Mexico"
,"New York"
,"North Carolina"
,"North Dakota"
,"Ohio"
,"Oklahoma"
,"Oregon"
,"Pennsylvania"
,"Rhode Island"
,"South Carolina"
,"South Dakota"
,"Tennessee"
,"Texas"
,"Utah"
,"Vermont"
,"Virginia"
,"Washington"
,"Washington DC"
,"West Virginia"
,"Wisconsin"
,"Wyoming"),
   index=None,
   placeholder="Select state...",
)
st.text_input("Zip Code")
st.text_area("Tell me about yourself:")



