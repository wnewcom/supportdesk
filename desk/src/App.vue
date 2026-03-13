<template>
  <FrappeUIProvider>
    <div class="min-h-screen bg-gray-50">
      <router-view />
    </div>
  </FrappeUIProvider>
</template>

<script setup>
import { FrappeUIProvider } from "frappe-ui";
</script>
