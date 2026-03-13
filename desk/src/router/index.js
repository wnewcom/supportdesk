import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Tickets",
    component: () => import("@/pages/PortalTickets.vue"),
    meta: { auth: true },
  },
  {
    path: "/tickets",
    name: "TicketsList",
    component: () => import("@/pages/PortalTickets.vue"),
    meta: { auth: true },
  },
  {
    path: "/ticket/:ticketId",
    name: "TicketDetail",
    component: () => import("@/pages/PortalTicketDetail.vue"),
    props: true,
    meta: { auth: true },
  },
  {
    path: "/new-ticket",
    name: "NewTicket",
    component: () => import("@/pages/PortalNewTicket.vue"),
    meta: { auth: true },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    redirect: "/tickets",
  },
];

export const router = createRouter({
  history: createWebHistory("/supportdesk/"),
  routes,
});

const LOGIN_PAGE = "/login";

router.beforeEach((to, _from, next) => {
  const user = window.session_user || window.frappe?.session?.user;
  if (to.meta.auth && user === "Guest") {
    const redirect = encodeURIComponent("/supportdesk" + (to.fullPath !== "/" ? to.fullPath : "/tickets"));
    window.location.href = `${LOGIN_PAGE}?redirect-to=${redirect}`;
    return;
  }
  next();
});
