<template>
  <div class="container mx-auto max-w-4xl px-4 py-8">
    <nav class="mb-4 flex items-center gap-2 text-sm text-gray-500">
      <RouterLink to="/tickets" class="hover:text-gray-700">
        Your Tickets
      </RouterLink>
      <span>/</span>
      <span class="text-gray-700">{{ ticketId }}</span>
    </nav>

    <div v-if="ticket.loading" class="text-center text-gray-500">
      Loading...
    </div>
    <template v-else-if="ticket.data">
      <div class="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 class="text-2xl font-semibold text-gray-900">
            {{ ticket.data.subject || ticketId }}
          </h1>
          <div class="mt-2 flex flex-wrap items-center gap-2">
            <Badge
              :label="ticket.data.status || '—'"
              :variant="statusVariant(ticket.data.status)"
            />
            <Badge
              v-if="ticket.data.priority"
              :label="ticket.data.priority"
              variant="gray"
            />
          </div>
        </div>
        <RouterLink to="/tickets">
          <Button variant="outline" theme="gray">Back to Your Tickets</Button>
        </RouterLink>
      </div>

      <div class="mb-6 rounded-lg border border-gray-200 bg-white shadow-sm">
        <div class="border-b border-gray-200 bg-gray-50 px-4 py-3">
          <h2 class="font-medium text-gray-900">Description</h2>
        </div>
        <div
          class="prose prose-sm max-w-none p-4"
          v-html="ticket.data.description || 'No description provided.'"
        />
      </div>

      <div
        v-if="
          ticket.data.checklist_items && ticket.data.checklist_items.length > 0
        "
        class="mb-6 rounded-lg border border-gray-200 bg-white shadow-sm"
      >
        <div class="border-b border-gray-200 bg-gray-50 px-4 py-3">
          <h2 class="font-medium text-gray-900">Job Checklist</h2>
        </div>
        <ul class="list-inside list-disc space-y-1 p-4">
          <li
            v-for="(item, i) in ticket.data.checklist_items"
            :key="i"
            class="flex items-center gap-2"
          >
            <span
              :class="item.completed ? 'text-green-600' : 'text-gray-400'"
            >
              {{ item.completed ? "✓" : "○" }}
            </span>
            {{ item.task_description || "—" }}
          </li>
        </ul>
      </div>
      <p
        v-else
        class="rounded-lg border border-gray-200 bg-white p-4 text-sm text-gray-500"
      >
        No checklist items for this ticket.
      </p>

      <RouterLink to="/tickets">
        <Button variant="outline" theme="gray">Back to Your Tickets</Button>
      </RouterLink>
    </template>
    <div v-else class="text-center text-gray-500">
      Ticket not found or you don't have permission to view it.
    </div>
  </div>
</template>

<script setup>
import { Badge, Button, createResource } from "frappe-ui";
import { RouterLink } from "vue-router";

const props = defineProps({
  ticketId: { type: String, required: true },
});

const ticket = createResource({
  url: "supportdesk.portal.portal_api.get_ticket",
  params: { name: () => props.ticketId },
  auto: true,
});

function statusVariant(status) {
  if (!status) return "gray";
  const s = status.toLowerCase().replace(/\s/g, "-");
  if (s === "open") return "blue";
  if (s === "in-progress") return "green";
  if (s === "pending") return "yellow";
  if (s === "resolved") return "green";
  if (s === "closed") return "gray";
  return "gray";
}
</script>
