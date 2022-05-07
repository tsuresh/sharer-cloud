import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import AuthLayout from '@/layout/auth-layout.vue'
import AppLayout from '@/layout/app-layout.vue'
import Page404Layout from '@/layout/page-404-layout.vue'

import RouteViewComponent from './route-view.vue'
import UIRoute from '@/pages/admin/ui/route'

const routes: Array<RouteRecordRaw> = [
  {
    path: "/:catchAll(.*)",
    redirect: { name: 'dashboard' },
  },
  {
    name: 'admin',
    path: '/admin',
    component: AppLayout,
    children: [
      {
        name: 'dashboard',
        path: 'dashboard',
        component: () => import('@/pages/admin/dashboard/Dashboard.vue'),
      },
      {
        name: 'request',
        path: 'request',
        component: () => import('@/pages/admin/request/RequestProcess.vue'),
      },
      {
        name: 'network',
        path: 'network',
        component: () => import('@/pages/admin/network/data-tables/Network.vue'),
      },
      {
        name: 'workloads',
        path: 'workloads',
        component: () => import('@/pages/admin/workloads/data-tables/Workloads.vue'),
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  //  mode: process.env.VUE_APP_ROUTER_MODE_HISTORY === 'true' ? 'history' : 'hash',
  routes
})

export default router
