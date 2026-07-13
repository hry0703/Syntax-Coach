import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import ChatPage from '../pages/ChatPage.vue'
import MistakesPage from '../pages/MistakesPage.vue'
import ReviewPage from '../pages/ReviewPage.vue'
import HistoryPage from '../pages/HistoryPage.vue'
import SettingsPage from '../pages/SettingsPage.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomePage },
    { path: '/chat/:sceneId', name: 'chat', component: ChatPage },
    { path: '/mistakes', name: 'mistakes', component: MistakesPage },
    { path: '/review', name: 'review', component: ReviewPage },
    { path: '/history', name: 'history', component: HistoryPage },
    { path: '/settings', name: 'settings', component: SettingsPage },
  ],
})
