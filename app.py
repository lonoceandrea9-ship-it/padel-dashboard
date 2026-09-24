import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import hashlib
import os
import time
import psycopg2
import psycopg2.extras

# Streamlit page configuration
st.set_page_config(
    page_title="Nac Team Performance App",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="auto"
)
