import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 페이지 설정
st.set_page_config(page_title="ClassicModels Dashboard", layout="wide")

# 데이터베이스 연결 함수
@st.cache_data
def load_data():
    conn = sqlite3.connect('classicmodels.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    data = {}
    for table in tables:
        table_name = table[0]
        query = f"SELECT * FROM {table_name}"
        data[table_name] = pd.read_sql_query(query, conn)
    
    conn.close()
    return data

# 데이터 로드
data = load_data()

# 사이드바
st.sidebar.title("ClassicModels Dashboard")
selected_table = st.sidebar.selectbox(
    "Select Table",
    list(data.keys())
)

# 메인 컨텐츠
st.title("ClassicModels Data Analysis")

# 선택된 테이블의 데이터 표시
st.subheader(f"Data from {selected_table} table")
st.dataframe(data[selected_table].head())

# 테이블별 시각화
if selected_table == 'customers':
    st.subheader("Customer Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 국가별 고객 수
        country_counts = data['customers']['country'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=country_counts.values, y=country_counts.index, ax=ax)
        plt.title('Top 10 Countries by Number of Customers')
        plt.xlabel('Number of Customers')
        st.pyplot(fig)
    
    with col2:
        # 신용한도 분포
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data['customers']['creditLimit'], bins=30, ax=ax)
        plt.title('Distribution of Credit Limits')
        plt.xlabel('Credit Limit')
        st.pyplot(fig)

elif selected_table == 'products':
    st.subheader("Product Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 제품 라인별 평균 가격
        product_line_prices = data['products'].groupby('productLine')['MSRP'].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=product_line_prices.values, y=product_line_prices.index, ax=ax)
        plt.title('Average MSRP by Product Line')
        plt.xlabel('Average MSRP')
        st.pyplot(fig)
    
    with col2:
        # 재고 수준
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x='productLine', y='quantityInStock', data=data['products'], ax=ax)
        plt.title('Stock Levels by Product Line')
        plt.xticks(rotation=45)
        st.pyplot(fig)

elif selected_table == 'orders':
    st.subheader("Order Analysis")
    
    # 날짜 변환
    data['orders']['orderDate'] = pd.to_datetime(data['orders']['orderDate'])
    data['orders']['month'] = data['orders']['orderDate'].dt.to_period('M')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 월별 주문 수
        monthly_orders = data['orders']['month'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        monthly_orders.plot(kind='line', marker='o', ax=ax)
        plt.title('Number of Orders by Month')
        plt.xlabel('Month')
        plt.ylabel('Number of Orders')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        # 주문 상태 분포
        status_counts = data['orders']['status'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=status_counts.values, y=status_counts.index, ax=ax)
        plt.title('Order Status Distribution')
        plt.xlabel('Number of Orders')
        st.pyplot(fig)

elif selected_table == 'orderdetails':
    st.subheader("Order Details Analysis")
    
    # 주문 금액 계산
    data['orderdetails']['total_amount'] = data['orderdetails']['quantityOrdered'] * data['orderdetails']['priceEach']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 주문 금액 분포
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data['orderdetails']['total_amount'], bins=30, ax=ax)
        plt.title('Distribution of Order Amounts')
        plt.xlabel('Order Amount')
        plt.ylabel('Frequency')
        st.pyplot(fig)
    
    with col2:
        # 주문 수량 분포
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(y='quantityOrdered', data=data['orderdetails'], ax=ax)
        plt.title('Distribution of Order Quantities')
        plt.ylabel('Quantity Ordered')
        st.pyplot(fig)

# 통계 정보 표시
st.sidebar.subheader("Table Statistics")
st.sidebar.write(f"Total rows: {len(data[selected_table])}")
st.sidebar.write(f"Columns: {', '.join(data[selected_table].columns)}")