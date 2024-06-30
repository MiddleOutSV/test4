import yfinance as yf
from transformers import pipeline
import streamlit as st
import requests

def fetch_news(ticker, period='1d'):
    stock = yf.Ticker(ticker)
    try:
        news = stock.news
    except requests.exceptions.JSONDecodeError:
        st.error("뉴스 데이터를 가져오는 데 문제가 발생했습니다. 잠시 후 다시 시도하세요.")
        return []
    
    if period == '1d':
        return news[:10]  # 뉴스 목록에서 최근 10개를 가져옵니다.
    elif period == '1wk':
        return news[:50]  # 최근 50개
    elif period == '1mo':
        return news[:200]  # 최근 200개
    return news

def summarize_news(news_list):
    summarizer = pipeline("summarization")
    summaries = []
    for news in news_list:
        try:
            summary = summarizer(news['summary'], max_length=50, min_length=25, do_sample=False)[0]['summary_text']
        except Exception as e:
            summary = "요약을 생성하는 데 실패했습니다."
        summaries.append({"title": news['title'], "summary": summary, "link": news['link']})
    return summaries

def main():
    st.title('주식 뉴스 요약 앱')
    
    ticker = st.text_input('주식 Ticker를 입력하세요 (예: AAPL)')
    period = st.selectbox('기간을 선택하세요', ['1d', '1wk', '1mo'])
    
    if st.button('뉴스 가져오기'):
        with st.spinner('뉴스를 가져오는 중...'):
            news_list = fetch_news(ticker, period)
            if news_list:
                summaries = summarize_news(news_list)
                st.success('뉴스 가져오기 완료!')
                
                for news in summaries:
                    st.subheader(news['title'])
                    st.write(news['summary'])
                    st.write(f"[링크]({news['link']})")

if __name__ == '__main__':
    main()
