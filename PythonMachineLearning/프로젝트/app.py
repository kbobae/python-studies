import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb 
#tmdb 데이터를 쓰기 위해 Movie, TMDb 객체를 생성하여 초기화 해야 함

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '0ee6a32fe14b93379e743072a6c9cf58'
tmdb.language = 'ko-KR'
#프로그램이 서버에 데이터를 요청하면 서버가 반환해주는데 서로 통신할 수 있게 해줌

def get_recommendations(title):
    # 영화 제목을 통해서 전체 데이터 기준 그 영화의 index 값을 얻기
    idx = movies[movies['title'] == title].index[0]
    
    # 코사인 유사도 매트릭스 (cosine_sim) 에서 idx 에 해당하는 데이터를 (idx, 유사도) 형태로 얻기
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # 코사인 유사도 기준으로 내림차순 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # 자기 자신을 제외한 10개의 추천 영화를 슬라이싱
    sim_scores = sim_scores[1:11]
    
    # 추천 영화 목록 10개의 인덱스 정보 추출
    movie_indices = [i[0] for i in sim_scores]
    
    # 인덱스 정보를 통해 영화 제목 추출
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i]
        details = movie.details(id)

        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'no_image.jpg'

        images.append(image_path)
        titles.append(details['title']) #tmdb는 언어설정을 하면 한국어로 받아올 수 있음

    return images, titles

#데이터 준비
movies = pickle.load(open('movies.pickle', 'rb')) #movies.pickle 파일을 읽기모드로 불러옴
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

st.set_page_config(layout='wide') #전체화면
st.header('CineMatch')

#페이지에서 영화 제목 선택 후 버튼 클릭 시 컨텐츠 기반 필터링 방식으로 해당 영화와 추천 영화를 보여줌

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)
if st.button('Recommend'):
    with st.spinner('Please wait...'): #프로그래스바
        images, titles = get_recommendations(title)

        idx = 0
        for i in range(0, 2):
            cols = st.columns(5) #5개의 컬럼을 만들어줌
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1