<template>
  <div class="container mx-auto max-w-4xl px-4 py-8">
    <div class="mb-6 flex flex-wrap items-start justify-between gap-4">
      <div>
        <h1 class="text-2xl font-semibold text-gray-900">
          Your Support Tickets
        </h1>
        <p class="mt-1 text-sm text-gray-500">
          Check status and track your repair or support requests.
        </p>
      </div>
      <RouterLink to="/new-ticket">
        <Button variant="solid" theme="blue">Submit New Request</Button>
      </RouterLink>
    </div>

    <div class="rounded-lg border border-gray-200 bg-white shadow-sm">
      <div v-if="tickets.loading" class="p-8 text-center text-gray-500">
        Loading...
      </div>
      <div
        v-else-if="!tickets.data || tickets.data.length === 0"
        class="p-8 text-center text-gray-500"
      >
        <p>No tickets yet. Submit a request and we'll get back to you.</p>
        <RouterLink to="/new-ticket" class="mt-4 inline-block">
          <Button variant="outline" theme="gray">Submit New Request</Button>
        </RouterLink>
      </div>
      <ul v-else class="divide-y divide-gray-200">
        <li
          v-for="t in tickets.data"
          :key="t.name"
          class="transition-colors hover:bg-gray-50"
        >
          <RouterLink
            :to="{ name: 'TicketDetail', params: { ticketId: t.name } }"
            class="flex flex-wrap items-center gap-3 px-4 py-4 sm:px-6"
          >
            <div class="min-w-0 flex-1">
              <span class="font-semibold text-gray-900">{{
                t.ticket_id || t.name
              }}</span>
              <span class="ml-2 text-gray-600">{{ t.subject || "—" }}</span>
            </div>
            <div class="flex flex-shrink-0 items-center gap-2">
              <Badge :label="t.status || '—'" :variant="statusVariant(t.status)" />
              <span
                v-if="t.priority"
                class="rounded border border-gray-200 bg-gray-50 px-2 py-0.5 text-xs text-gray-600"
              >
                {{ t.priority }}
              </span>
              <span v-if="t.creation" class="text-xs text-gray-400">
                {{ formatDate(t.creation) }}
              </span>
              <span
                v-if="t.due_date"
                class="text-xs text-gray-400"
              >
                · Due: {{ formatDate(t.due_date) }}
              </span>
            </div>
          </RouterLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { Badge, Button, createResource } from "frappe-ui";
import { onMounted } from "vue";
import { RouterLink } from "vue-router";

const tickets = createResource({
  url: "supportdesk.portal.portal_api.get_my_tickets",
  auto: false,
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

function formatDate(d) {
  if (!d) return "";
  try {
    const s = typeof d === "string" ? d.split(" ")[0] : d;
    return new Date(s).toLocaleDateString();
  } catch {
    return d;
  }
}

onMounted(() => {
  tickets.reload();
});
</script>
