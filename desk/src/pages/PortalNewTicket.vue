<template>
  <div class="container mx-auto max-w-2xl px-4 py-8">
    <nav class="mb-4 flex items-center gap-2 text-sm text-gray-500">
      <RouterLink to="/tickets" class="hover:text-gray-700">
        Your Tickets
      </RouterLink>
      <span>/</span>
      <span class="text-gray-700">New Request</span>
    </nav>

    <h1 class="text-2xl font-semibold text-gray-900">
      Submit a Support Request
    </h1>
    <p class="mt-1 text-sm text-gray-500">
      Describe your issue or repair request. We'll get back to you as soon as we can.
    </p>

    <div class="mt-6 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <form @submit.prevent="onSubmit" class="space-y-4">
        <FormControl label="Subject" required>
          <input
            v-model="form.subject"
            type="text"
            class="w-full rounded border border-gray-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            placeholder="e.g. Laptop not turning on"
            required
          />
        </FormControl>
        <FormControl label="Description">
          <textarea
            v-model="form.description"
            class="w-full rounded border border-gray-200 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            rows="5"
            placeholder="Describe the issue in as much detail as you can."
          />
        </FormControl>
        <div class="flex gap-2">
          <Button
            type="submit"
            variant="solid"
            theme="blue"
            :loading="createTicket.loading"
          >
            {{ createTicket.loading ? "Submitting..." : "Submit Request" }}
          </Button>
          <RouterLink to="/tickets">
            <Button type="button" variant="outline" theme="gray">
              Cancel
            </Button>
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { Button, FormControl, createResource, toast } from "frappe-ui";
import { reactive } from "vue";
import { RouterLink, useRouter } from "vue-router";

const router = useRouter();
const form = reactive({
  subject: "",
  description: "",
});

const createTicket = createResource({
  url: "frappe.client.insert",
  onSuccess(data) {
    if (data && data.name) {
      toast.success("Request submitted.");
      router.push({ name: "TicketDetail", params: { ticketId: data.name } });
    }
  },
  onError(err) {
    toast.error(err.message || "Something went wrong. Please try again.");
  },
});

function onSubmit() {
  if (!form.subject?.trim()) return;
  createTicket.submit({
    doc: {
      doctype: "Ticket",
      subject: form.subject.trim(),
      description: form.description || "",
      status: "Open",
    },
  });
}
</script>
