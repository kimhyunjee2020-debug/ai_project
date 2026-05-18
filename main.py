import streamlit as st
st.title('나의 첫 웹 서비스 만들기')
a=st.text_input('이름을 입력해주세요')
b=st.selectbox('좋아하는 음식을 선택해주세요',['치킨','마라탕','피자','엽떡','곱창','마라샹궈','파스타','두쫀쿠','버터떡','스테이크','돼직고기'])
if st.button('인사말 생성'):
  st.write(a+'님,안녕하세요')
  st.info('반갑습니다')
  st.warning(b+'음식을 좋아하시나봐요')
  st.error('잘 부탁드립니다')
  st.ballons()
