<template>
  <div class="space-y-4 md:space-y-6">
    <!-- Email Metadata Card -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 md:p-6 hover:border-slate-600 transition-colors">
        <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 md:mb-4">Sender</h3>
        <p class="text-xs md:text-sm text-white truncate font-mono" :title="metadata.sender">{{ metadata.sender }}</p>
      </div>
      <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 md:p-6 hover:border-slate-600 transition-colors">
        <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 md:mb-4">Subject</h3>
        <p class="text-xs md:text-sm text-white truncate" :title="metadata.subject">{{ metadata.subject }}</p>
      </div>
      <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 md:p-6 hover:border-slate-600 transition-colors">
        <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 md:mb-4">Attachments</h3>
        <p class="text-2xl font-bold text-white">{{ metadata.attachment_count }}</p>
        <p class="text-xs text-slate-400 mt-1">{{ metadata.has_attachments ? 'Present' : 'None' }}</p>
      </div>
    </div>

    <!-- Analysis Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
      <!-- Phishing Analysis -->
      <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 md:p-6">
        <div class="flex items-center justify-between mb-3 md:mb-4 gap-2">
          <h3 class="text-base md:text-lg font-semibold text-white">🎣 Phishing Analysis</h3>
          <span 
            class="px-2 md:px-3 py-1 rounded-full text-xs font-bold uppercase whitespace-nowrap"
            :class="getPhishingBadgeClass"
          >
            {{ phishing.level }}
          </span>
        </div>
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-slate-300 text-sm">Risk Score</span>
            <span class="text-xl md:text-2xl font-bold" :class="getPhishingColor">{{ phishing.score }}/100</span>
          </div>
          <div class="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
            <div 
              class="h-full rounded-full transition-all duration-300"
              :style="{ 
                width: phishing.score + '%',
                background: getPhishingGradient
              }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Spam Analysis -->
      <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 md:p-6">
        <div class="flex items-center justify-between mb-3 md:mb-4 gap-2">
          <h3 class="text-base md:text-lg font-semibold text-white">📧 Spam Analysis</h3>
          <span 
            class="px-2 md:px-3 py-1 rounded-full text-xs font-bold uppercase whitespace-nowrap"
            :class="getSpamBadgeClass"
          >
            {{ spam.level }}
          </span>
        </div>
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-slate-300 text-sm">Spam Score</span>
            <span class="text-xl md:text-2xl font-bold" :class="getSpamColor">{{ spam.score }}/100</span>
          </div>
          <div class="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
            <div 
              class="h-full rounded-full transition-all duration-300"
              :style="{ 
                width: spam.score + '%',
                background: getSpamGradient
              }"
            ></div>
          </div>
          <p class="text-xs text-slate-400">Probability: {{ (spam.probability * 100).toFixed(0) }}%</p>
        </div>
      </div>
    </div>

    <!-- Phishing Findings -->
    <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 md:p-6">
      <div class="flex items-center justify-between mb-3 md:mb-4 gap-2">
        <h3 class="text-base md:text-lg font-semibold text-white">🎣 Phishing Findings</h3>
        <span class="text-xs font-semibold text-slate-400">{{ phishing.findings.length }} findings</span>
      </div>
      <div v-if="phishing.findings.length === 0" class="text-slate-400 italic text-sm">
        No phishing indicators detected.
      </div>
      <ul v-else class="space-y-2 max-h-64 overflow-y-auto">
        <li 
          v-for="(finding, idx) in phishing.findings" 
          :key="`phishing-${idx}`"
          class="flex items-start gap-2 md:gap-3 text-xs md:text-sm p-2 md:p-3 bg-red-500/10 border border-red-500/20 rounded-lg hover:border-red-500/40 transition-colors"
        >
          <span class="text-lg flex-shrink-0 mt-0.5">⚠️</span>
          <span class="text-slate-200">{{ finding }}</span>
        </li>
      </ul>
    </div>

    <!-- Spam Findings -->
    <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 md:p-6">
      <div class="flex items-center justify-between mb-3 md:mb-4 gap-2">
        <h3 class="text-base md:text-lg font-semibold text-white">📧 Spam Findings</h3>
        <span class="text-xs font-semibold text-slate-400">{{ spam.findings.length }} findings</span>
      </div>
      <div v-if="spam.findings.length === 0" class="text-slate-400 italic text-sm">
        No spam indicators detected.
      </div>
      <ul v-else class="space-y-2 max-h-64 overflow-y-auto">
        <li 
          v-for="(finding, idx) in spam.findings" 
          :key="`spam-${idx}`"
          class="flex items-start gap-2 md:gap-3 text-xs md:text-sm p-2 md:p-3 bg-orange-500/10 border border-orange-500/20 rounded-lg hover:border-orange-500/40 transition-colors"
        >
          <span class="text-lg flex-shrink-0 mt-0.5">🚩</span>
          <span class="text-slate-200">{{ finding }}</span>
        </li>
      </ul>
    </div>

    <!-- Technical Details -->
    <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 md:p-6">
      <h3 class="text-base md:text-lg font-semibold text-white mb-3 md:mb-4">📊 Technical Details</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4 text-sm">
        <div class="bg-slate-700/50 rounded-lg p-3">
          <p class="text-slate-400 text-xs uppercase font-semibold">URLs Found</p>
          <p class="text-white text-lg md:text-2xl font-bold mt-1 md:mt-2">{{ metadata.url_count }}</p>
        </div>
        <div class="bg-slate-700/50 rounded-lg p-3">
          <p class="text-slate-400 text-xs uppercase font-semibold">Attachments</p>
          <p class="text-white text-lg md:text-2xl font-bold mt-1 md:mt-2">{{ metadata.attachment_count }}</p>
        </div>
        <div class="bg-slate-700/50 rounded-lg p-3">
          <p class="text-slate-400 text-xs uppercase font-semibold truncate">Classification</p>
          <p class="text-white text-xs md:text-sm font-bold mt-1 md:mt-2 break-words">{{ classification }}</p>
        </div>
        <div class="bg-slate-700/50 rounded-lg p-3">
          <p class="text-slate-400 text-xs uppercase font-semibold">Risk Level</p>
          <p class="text-white text-xs md:text-sm font-bold mt-1 md:mt-2">{{ getRiskLevel }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  metadata: Object,
  phishing: Object,
  spam: Object,
  classification: String
})

const getPhishingColor = computed(() => {
  if (props.phishing.score >= 70) return 'text-red-400'
  if (props.phishing.score >= 50) return 'text-orange-400'
  if (props.phishing.score >= 30) return 'text-yellow-400'
  return 'text-green-400'
})

const getSpamColor = computed(() => {
  if (props.spam.score >= 80) return 'text-red-400'
  if (props.spam.score >= 50) return 'text-orange-400'
  if (props.spam.score >= 30) return 'text-yellow-400'
  return 'text-green-400'
})

const getPhishingBadgeClass = computed(() => {
  if (props.phishing.level === 'CRITICAL') return 'bg-red-500/30 text-red-200'
  if (props.phishing.level === 'HIGH') return 'bg-orange-500/30 text-orange-200'
  if (props.phishing.level === 'MEDIUM') return 'bg-yellow-500/30 text-yellow-200'
  if (props.phishing.level === 'LOW') return 'bg-blue-500/30 text-blue-200'
  return 'bg-green-500/30 text-green-200'
})

const getSpamBadgeClass = computed(() => {
  if (props.spam.level === 'LIKELY_SPAM') return 'bg-red-500/30 text-red-200'
  if (props.spam.level === 'SUSPICIOUS') return 'bg-orange-500/30 text-orange-200'
  if (props.spam.level === 'LOW_RISK') return 'bg-yellow-500/30 text-yellow-200'
  return 'bg-green-500/30 text-green-200'
})

const getPhishingGradient = computed(() => {
  if (props.phishing.score >= 70) return 'linear-gradient(90deg, #ef4444, #dc2626)'
  if (props.phishing.score >= 50) return 'linear-gradient(90deg, #f97316, #ea580c)'
  if (props.phishing.score >= 30) return 'linear-gradient(90deg, #eab308, #ca8a04)'
  return 'linear-gradient(90deg, #22c55e, #16a34a)'
})

const getSpamGradient = computed(() => {
  if (props.spam.score >= 80) return 'linear-gradient(90deg, #ef4444, #dc2626)'
  if (props.spam.score >= 50) return 'linear-gradient(90deg, #f97316, #ea580c)'
  if (props.spam.score >= 30) return 'linear-gradient(90deg, #eab308, #ca8a04)'
  return 'linear-gradient(90deg, #22c55e, #16a34a)'
})

const getRiskLevel = computed(() => {
  const score = Math.max(props.phishing.score, props.spam.score)
  if (score >= 70) return 'CRITICAL'
  if (score >= 50) return 'HIGH'
  if (score >= 30) return 'MEDIUM'
  return 'LOW'
})
</script>
