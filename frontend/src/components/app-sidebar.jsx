import * as React from "react"
import {
  AudioWaveform,
  BookOpen,
  Bot,
  Command,
  Frame,
  GalleryVerticalEnd,
  Map,
  PieChart,
  Settings2,
  SquareTerminal,
  ChevronRight,
  Home,
  User,
  Monitor,
  Cog,
  CreditCard,
  BarChart2,
  Scale,
  Building2,
  Briefcase,
  Shield,
  Grid,
} from "lucide-react"

import { NavMain } from "@/components/nav-main"
import { NavProjects } from "@/components/nav-projects"
import { NavUser } from "@/components/nav-user"
import { TeamSwitcher } from "@/components/team-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"

// This is sample data.
const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  teams: [
    {
      name: "Zero Q",
      logo: GalleryVerticalEnd,
      plan: "Enterprise",
    },
    {
      name: "Acme Corp.",
      logo: AudioWaveform,
      plan: "Startup",
    },
    {
      name: "Evil Corp.",
      logo: Command,
      plan: "Free",
    },
  ],
  navMain: [
    {
      title: "Playground",
      url: "#",
      icon: SquareTerminal,
      isActive: true,
      items: [
        {
          title: "History",
          url: "#",
        },
        {
          title: "Starred",
          url: "#",
        },
        {
          title: "Settings",
          url: "#",
        },
      ],
    },
    {
      title: "Models",
      url: "#",
      icon: Bot,
      items: [
        {
          title: "Genesis",
          url: "#",
        },
        {
          title: "Explorer",
          url: "#",
        },
        {
          title: "Quantum",
          url: "#",
        },
      ],
    },
    {
      title: "Documentation",
      url: "#",
      icon: BookOpen,
      items: [
        {
          title: "Introduction",
          url: "#",
        },
        {
          title: "Get Started",
          url: "#",
        },
        {
          title: "Tutorials",
          url: "#",
        },
        {
          title: "Changelog",
          url: "#",
        },
      ],
    },
    {
      title: "Settings",
      url: "#",
      icon: Settings2,
      items: [
        {
          title: "General",
          url: "#",
        },
        {
          title: "Team",
          url: "#",
        },
        {
          title: "Billing",
          url: "#",
        },
        {
          title: "Limits",
          url: "#",
        },
      ],
    },
  ],
  projects: [
    {
      name: "Design Engineering",
      url: "#",
      icon: Frame,
    },
    {
      name: "Sales & Marketing",
      url: "#",
      icon: PieChart,
    },
    {
      name: "Travel",
      url: "#",
      icon: Map,
    },
  ],
}

function SidebarItem({ icon: Icon, label, active }) {
  return (
    <div
      className={`flex items-center justify-between px-4 py-3 mb-1 cursor-pointer transition-colors
        ${active
          ? "bg-[#4B6FEA] text-white rounded-xl"
          : "hover:bg-[#35373a] text-white rounded-lg"
        }`}
    >
      <div className="flex items-center gap-3">
        <Icon className="w-5 h-5" />
        <span className="text-base">{label}</span>
      </div>
      <ChevronRight className="w-4 h-4 opacity-70" />
    </div>
  )
}

export function AppSidebar({
  ...props
}) {
  return (
    <Sidebar collapsible="icon" className="bg-[#232526] text-white border-r border-gray-700" {...props}>
      <SidebarHeader className="border-b border-gray-700">
        {/* Header with Logo */}
        <div className="flex items-center gap-3 p-2">
          <div className="w-8 h-8 bg-gray-200 rounded-lg flex items-center justify-center">
            <img src="https://zeroq.hfapp.net/logo.svg" width="20px" height="20px" alt="ZeroQ Logo" />
          </div>
          <span className="text-xl font-medium text-white">Zero Q</span>
        </div>
      </SidebarHeader>
      <SidebarContent className="overflow-visible">
        <NavMain items={data.navMain} />
        <NavProjects projects={data.projects} />
      </SidebarContent>
      <SidebarFooter className="border-t border-gray-700">
        <NavUser user={data.user} />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
