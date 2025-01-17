<template>
  <div v-if="isLoaded" class="profile-page">
    <!-- 히어로 섹션 -->
    <div class="profile-hero position-relative">
      <div class="hero-overlay"></div>
      <div class="container hero-content">
        <div class="row align-items-center">
          <div class="col-md-3">
            <!-- 프로필 이미지 -->
            <div class="profile-image-container">
              <!-- 이미지 없으면 기본이미지로 -->
              <img :src="profile_img || '/default-profile.png'" :alt="name" class="profile-image" />
              <!-- <img :src="store.API_URL + image.image" :alt="image.description" /> -->
              <!-- 이미지 편집 -->
              <div v-if="showEditButton" class="image-overlay">
                <label for="profile-image-input" class="edit-image-btn">
                  <i class="fas fa-pencil-alt"></i>
                </label>
                <input type="file" id="profile-image-input" accept="image/*" @change="handleImageChange" class="hidden-input" />
              </div>
            </div>
          </div>
          <div class="col-md-9">
            <h1 class="profile-name text-white mb-2">{{ name }}</h1>
            <p class="username text-white-50 mb-1">@{{ username }}</p>
            <p class="email text-white-50 mb-4">{{ email }}</p>

            <div class="d-flex gap-4 mb-4">
              <div class="stat-badge">
                <!-- <span class="stat-value">{{ articles.count }}</span> -->
                <span class="stat-value">{{ articles_count }}</span>
                <span class="stat-label">게시글</span>
              </div>
              <div class="stat-badge">
                <span class="stat-value">{{ followers_count }}</span>
                <span class="stat-label">팔로워</span>
              </div>
              <div class="stat-badge">
                <span class="stat-value">{{ followings_count }}</span>
                <span class="stat-label">팔로잉</span>
              </div>
            </div>

            <!-- 팔로잉 팔로워 버튼 -->
            <button v-if="showFollowButton" @click="follow" :class="['follow-btn', is_following ? 'following' : '']">
              <i :class="['fas', is_following ? 'fa-user-minus' : 'fa-user-plus']"></i>
              {{ is_following ? "언팔로우" : "팔로우" }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 메인 컨텐츠 -->
    <div class="container py-5">
      <!-- 내가 작성한 글 섹션 -->
      <section class="content-section mb-5">
        <h2 class="section-title">최근 작성한 글</h2>
        <!-- v-if -->
        <div v-if="sortedArticles.length > 0" class="row g-4">
          <div class="col-md-4" v-for="article in sortedArticles" :key="article.id">
            <RouterLink
              :to="{
                name: 'GroupWatchedMovie',
                params: {
                  group_id: article.group_movie.group_id,
                  group_movie_id: article.group_movie.id,
                },
              }"
            >
              <div class="review-card">
                <div class="review-header">
                  <h3 class="movie-title">{{ article.group_movie.movie_title }}</h3>
                  <span class="created-at">{{ getRelativeTime(article.created_at) }}</span>
                </div>
                <p class="review-excerpt">{{ article.content }}</p>
              </div>
            </RouterLink>
          </div>
        </div>
        <!-- v-else는 v-if와 같은 수준에 위치 -->
        <div v-else class="text-center text-muted py-5">아직 작성한 게시글이 없습니다.</div>
      </section>

      <!-- 찜한 영화 섹션 -->
      <section class="content-section">
        <h2 class="section-title">찜한 영화 목록</h2>
        <div v-if="likedMovies.length > 0" class="row g-4">
          <div class="col-md-3" v-for="(likedMovie, index) in likedMovies" :key="index">
            <RouterLink :to="{ name: 'MovieDetailView', params: { movieId: likedMovie.movie_id } }">
              <div class="movie-card">
                <div class="movie-poster">
                  <img :src="'https://image.tmdb.org/t/p/original/' + likedMovie.poster_path" alt="Movie poster" />
                  <div class="movie-overlay">
                    <button class="play-btn">
                      <i class="fas fa-info-circle"></i>
                    </button>
                  </div>
                </div>
                <div class="movie-info">
                  <h3 class="movie-title">{{ likedMovie.title }}</h3>
                </div>
              </div>
            </RouterLink>
          </div>
        </div>
        <div v-else class="text-center text-muted py-5">아직 찜한 영화가 없습니다.</div>
      </section>

      <!-- 회원탈퇴 버튼 -->
      <div class="text-center mt-5">
        <button v-if="showDeleteButton" @click="deleteAccount" class="delete-account-btn">회원탈퇴</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useCounterStore } from "@/stores/counter";
// 상대적 시간 표시 라이브러리 ------
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import "dayjs/locale/ko"; // 한국어 로케일

dayjs.extend(relativeTime);
dayjs.locale("ko");
// ** npm install dayjs 필요 **
// ------------------------------

// 상태 관리
const route = useRoute();
const store = useCounterStore();
const isLoaded = ref(false);

// 프로필 데이터
const id = ref(null);
const name = ref(null);
const username = ref(null);
const email = ref(null);
const profile_img = ref(null);
const followers_count = ref(0);
const followings_count = ref(0);
const is_following = ref(false);
const articles_count = ref(0);
const articles = ref([]);
const group_movie = ref(null);
const likedMovies = ref([]);

// 계산된 속성
const showFollowButton = computed(() => {
  return id.value && store.currentUser?.id && id.value !== store.currentUser.id;
});

const showDeleteButton = computed(() => {
  return id.value && store.currentUser?.id && id.value === store.currentUser.id;
});

const showEditButton = computed(() => {
  return id.value && store.currentUser?.id && id.value === store.currentUser.id;
});

// 최근에 쓴 글이 제일 앞에 오도록
const sortedArticles = computed(() => {
  return [...articles.value].sort((a, b) => {
    return new Date(b.created_at) - new Date(a.created_at);
  });
});

// 상대 시간 계산 함수
const getRelativeTime = (date) => {
  const now = dayjs();
  const createdDate = dayjs(date);

  // 24시간 이내인 경우
  if (now.diff(createdDate, "day") === 0) {
    if (now.diff(createdDate, "hour") === 0) {
      return `${now.diff(createdDate, "minute")}분 전`;
    }
    return `${now.diff(createdDate, "hour")}시간 전`;
  }
  // 어제인 경우
  else if (now.diff(createdDate, "day") === 1) {
    return "어제";
  }
  // 7일 이내인 경우
  else if (now.diff(createdDate, "day") < 7) {
    return `${now.diff(createdDate, "day")}일 전`;
  }
  // 그 외의 경우 날짜 표시
  return createdDate.format("YYYY.MM.DD");
};

// 이미지 업로드 처리
const handleImageChange = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // 파일 크기 체크 (5MB 제한)
  // if (file.size > 5 * 1024 * 1024) {
  //   alert("파일 크기는 5MB 이하여야 합니다.");
  //   return;
  // }

  // 이미지 파일 타입 체크
  if (!file.type.startsWith("image/")) {
    alert("이미지 파일만 업로드 가능합니다.");
    return;
  }

  const formData = new FormData();
  formData.append("profile_img", file);

  // 이미지 수정 요청
  axios({
    method: "put",
    url: `http://127.0.0.1:8000/api/v2/${route.params.user_id}/profile/`,
    headers: {
      Authorization: `Token ${store.token}`,
      // 이미지가 포함된 요청일 때 필요함
      "Content-Type": "multipart/form-data",
    },
    data: formData,
  })
    .then((response) => {
      profile_img.value = store.API_URL + response.data.profile_img;
      alert("프로필 이미지가 업데이트되었습니다.");
    })
    .catch((error) => {
      console.error("이미지 업로드 실패:", error);
      alert("이미지 업로드에 실패했습니다. 다시 시도해주세요.");
    });
};

// 팔로우 요청
const follow = async () => {
  try {
    const response = await axios({
      method: "post",
      url: `http://127.0.0.1:8000/api/v2/${route.params.user_id}/follow/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });

    followers_count.value = response.data.followers_count;
    followings_count.value = response.data.followings_count;
    is_following.value = response.data.is_following;
  } catch (error) {
    console.error("팔로우 요청 실패:", error);
  }
};

// 계정 삭제
const deleteAccount = function () {
  if (id.value === store.currentUser.id) {
    store.deleteAccount(id.value);
  }
};

// 프로필 데이터 로드 : 설정해둔 프로필 이미지 조회
const loadProfileData = () => {
  axios({
    method: "get",
    url: `http://127.0.0.1:8000/api/v2/${route.params.user_id}/profile/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      const data = response.data;

      id.value = data.id;
      name.value = data.name;
      username.value = data.username;
      email.value = data.email;
      profile_img.value = data.profile_img;
      followers_count.value = data.followers_count;
      followings_count.value = data.followings_count;
      is_following.value = data.is_following;
      articles_count.value = data.articles_count;
      articles.value = data.articles;
      isLoaded.value = true;
      group_movie.value = data.group_movie;
      likedMovies.value = data.liked_movies;
      articles.value = data.articles; // articles 데이터 할당
      console.log("Loaded articles:", articles.value); // 데이터가 제대로 로드되었는지 확인
      console.log(response.data);
    })
    .catch((error) => {
      console.error("프로필 데이터 로드 실패:", error);
    });
};

onMounted(() => {
  loadProfileData();
});
</script>

<style scoped>
.profile-page {
  background-color: #f8f9fa;
}

.profile-hero {
  min-height: 400px;
  background: linear-gradient(45deg, #1a1a1a, #2c3e50);
  position: relative;
  margin-bottom: 2rem;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.3));
}

.hero-content {
  position: relative;
  padding: 4rem 0;
  z-index: 1;
}

.profile-image-container {
  position: relative;
  width: 220px;
  height: 220px;
  border-radius: 50%;
  margin: 0 auto;
}

.profile-image {
  width: 220px;
  height: 220px;
  border-radius: 50%;
  border: 4px solid #dc3545;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
  cursor: pointer;
}

.profile-image-container:hover .image-overlay {
  opacity: 1;
}

.edit-image-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #dc3545;
  transition: transform 0.2s ease;
}

.edit-image-btn:hover {
  transform: scale(1.1);
}

.hidden-input {
  display: none;
}

.profile-name {
  font-size: 2.5rem;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.stat-badge {
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
}

.stat-value {
  display: block;
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
}

.stat-label {
  display: block;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
}

.follow-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: 2px solid #dc3545;
  background: transparent;
  color: white;
  font-weight: 600;
  transition: all 0.2s;
}

.follow-btn.following {
  background: #dc3545;
}

.follow-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  position: relative;
}

.section-title::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -0.5rem;
  width: 50px;
  height: 3px;
  background: #dc3545;
}

.review-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.review-card:hover {
  transform: translateY(-5px);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.movie-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}
a {
  text-decoration: none;
  color: black;
}

.review-excerpt {
  color: #6c757d;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.movie-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.movie-poster {
  position: relative;
  padding-top: 150%;
}

.movie-poster img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.movie-card:hover .movie-overlay {
  opacity: 1;
}

.play-btn {
  background: white;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: #dc3545;
  transition: transform 0.2s;
}

.play-btn:hover {
  transform: scale(1.1);
}

.movie-info {
  padding: 0.7rem 1rem;
}

.movie-info h3 {
  margin: 0;
  font-size: 0.9rem; /* 1.25rem에서 0.9rem으로 축소 */
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.movie-info .movie-title {
  font-size: 0.9rem;
  font-weight: 500;
}

.movie-meta {
  display: flex;
  justify-content: space-between;
  color: #6c757d;
  font-size: 0.875rem;
}

.delete-account-btn {
  background: transparent;
  border: 2px solid #dc3545;
  color: #dc3545;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s;
}

.delete-account-btn:hover {
  background: #dc3545;
  color: white;
}

/* 상대 시간 관련 css */
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.created-at {
  font-size: 0.85rem;
  color: #666;
  white-space: nowrap;
}

.movie-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  flex: 1;
  margin-right: 1rem;
}
/* 모바일 반응형 스타일 */
@media (max-width: 768px) {
  .profile-hero {
    min-height: auto;
  }

  .hero-content {
    padding: 2rem 0;
  }

  .profile-image-container {
    width: 160px;
    height: 160px;
    margin-bottom: 1.5rem;
  }

  .profile-name {
    font-size: 2rem;
  }

  .stat-badge {
    padding: 0.5rem 1rem;
  }

  .edit-image-btn {
    width: 32px;
    height: 32px;
  }

  .movie-meta {
    flex-direction: column;
    gap: 0.5rem;
  }

  .review-card {
    margin-bottom: 1rem;
  }

  .section-title {
    font-size: 1.25rem;
  }

  .review-excerpt {
    -webkit-line-clamp: 2;
  }

  .stat-badge {
    padding: 0.5rem 1rem;
  }
  /* 프로필 이미지 */
  .profile-image {
    border: none;
  }
  /* 편집 버튼 */
  .edit-image-btn {
    background: white;
    color: #bcbcbc;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  /* Dark mode 대비 */
  /* @media (prefers-color-scheme: dark) {
  .profile-page {
    background-color: #1a1a1a;
  }

  .review-card,
  .movie-card,
  .stat-item {
    background: #2d2d2d;
  }

  .movie-title,
  .section-title {
    color: #ffffff;
  }

  .review-excerpt,
  .movie-meta {
    color: #a0a0a0;
  } */
}
</style>
