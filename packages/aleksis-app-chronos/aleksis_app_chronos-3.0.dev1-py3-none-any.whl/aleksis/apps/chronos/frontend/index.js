import { hasPersonValidator } from "aleksis.core/routeValidators";

export default
  {
    meta: {
      inMenu: true,
      titleKey: "chronos.menu_title",
      icon: "mdi-school-outline",
      validators: [
        hasPersonValidator
      ]
    },
    children: [
      {
        path: "",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.allTimetables",
        meta: {
          inMenu: true,
          titleKey: "chronos.timetable.menu_title_all",
          icon: "mdi-grid",
          permission: "chronos.view_timetable_overview_rule",
        },
      },
      {
        path: "timetable/my/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.myTimetable",
        meta: {
          inMenu: true,
          titleKey: "chronos.timetable.menu_title_my",
          icon: "mdi-account-outline",
          permission: "chronos.view_my_timetable_rule",
        },
      },
      {
        path: "timetable/my/:year/:month/:day/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.myTimetableByDate",
      },
      {
        path: "timetable/:type_/:pk/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.timetable",
      },
      {
        path: "timetable/:type_/:pk/:year/:week/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.timetableByWeek",
      },
      {
        path: "timetable/:type_/:pk/print/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.timetablePrint",
      },
      {
        path: "timetable/:type_/:pk/:regular/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.timetableRegular",
      },
      {
        path: "lessons/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.lessonsDay",
        meta: {
          inMenu: true,
          titleKey: "chronos.lessons.menu_title_daily",
          icon: "mdi-calendar-outline",
          permission: "chronos.view_lessons_day_rule",
        },
      },
      {
        path: "lessons/:year/:month/:day/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.lessonsDayByDate",
      },
      {
        path: "lessons/:id_/:week/substitution/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.editSubstitution",
      },
      {
        path: "lessons/:id_/:week/substitution/delete/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.deleteSubstitution",
      },
      {
        path: "substitutions/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.substitutions",
        meta: {
          inMenu: true,
          titleKey: "chronos.substitutions.menu_title",
          icon: "mdi-update",
          permission: "chronos.view_substitutions_rule",
        },
      },
      {
        path: "substitutions/print/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.substitutionsPrint",
      },
      {
        path: "substitutions/:year/:month/:day/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.substitutionsByDate",
      },
      {
        path: "substitutions/:year/:month/:day/print/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.substitutionsPrintByDate",
      },
      {
        path: "supervisions/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.supervisionsDay",
        meta: {
          inMenu: true,
          titleKey: "chronos.supervisions.menu_title_daily",
          icon: "mdi-calendar-outline",
          permission: "chronos.view_supervisions_day_rule",
        },
      },
      {
        path: "supervisions/:year/:month/:day/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.supervisionsDayByDate",
      },
      {
        path: "supervisions/:id_/:week/substitution/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.editSupervisionSubstitution",
      },
      {
        path: "supervisions/:id_/:week/substitution/delete/",
        component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
        name: "chronos.deleteSupervisionSubstitution",
      },
    ],
  }