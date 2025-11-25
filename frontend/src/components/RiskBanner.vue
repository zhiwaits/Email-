<template>
  <div 
    class="rounded-2xl p-6 md:p-8 border-2 shadow-2xl backdrop-blur-xl transition-all duration-300"
    :class="riskClasses"
  >
    <!-- Header -->
    <div class="flex flex-col md:flex-row items-start justify-between gap-4 md:gap-6 mb-6 md:mb-8">
      <div class="flex items-start gap-4 md:gap-6 flex-1">
        <div class="text-4xl md:text-5xl flex-shrink-0">{{ riskIcon }}</div>
        <div class="min-w-0">
          <h2 class="text-2xl md:text-3xl lg:text-4xl font-bold break-words leading-tight" :class="textColorClass">
            {{ classification }}
          </h2>
          <p class="text-sm md:text-base mt-2 md:mt-3 leading-relaxed" :class="subtextColorClass">
            {{ classificationDescription }}
          </p>
        </div>
      </div>
      <div class="text-right flex-shrink-0 bg-white/10 backdrop-blur rounded-2xl p-4 md:p-6">
        <div class="text-3xl md:text-4xl lg:text-5xl font-bold" :class="textColorClass">
          {{ Math.max(spamScore, score) }}
        </div>
        <p class="text-xs md:text-sm uppercase tracking-widest font-bold mt-2 opacity-80" :class="subtextColorClass">
          Risk Score
        </p>
      </div>
    </div>

    <!-- Progress Bars -->
    <div class="space-y-4 md:space-y-6 mb-6 md:mb-8">
      <!-- Phishing Progress -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <p class="text-xs md:text-sm font-bold uppercase tracking-wider text-white/80">Phishing Detection</p>
          <span class="text-sm md:text-base font-bold" :class="getPhishingColor">{{ score }}/100</span>
        </div>
        <div class="w-full bg-slate-700/50 rounded-full h-3 md:h-4 overflow-hidden backdrop-blur">
          <div 
            class="h-full rounded-full transition-all duration-500 bg-gradient-to-r"
            :class="score >= 70 ? 'from-red-500 to-red-600' : score >= 50 ? 'from-orange-500 to-orange-600' : score >= 30 ? 'from-yellow-500 to-yellow-600' : 'from-green-500 to-green-600'"
            :style="`width: ${score}%`"
          ></div>
        </div>
      </div>

      <!-- Spam Progress -->
      <div>
        <div class="flex items-center justify-between mb-2">
          <p class="text-xs md:text-sm font-bold uppercase tracking-wider text-white/80">Spam Detection</p>
          <span class="text-sm md:text-base font-bold" :class="getSpamColor">{{ spamScore }}/100</span>
        </div>
        <div class="w-full bg-slate-700/50 rounded-full h-3 md:h-4 overflow-hidden backdrop-blur">
          <div 
            class="h-full rounded-full transition-all duration-500 bg-gradient-to-r"
            :class="spamScore >= 80 ? 'from-red-500 to-red-600' : spamScore >= 50 ? 'from-orange-500 to-orange-600' : spamScore >= 30 ? 'from-yellow-500 to-yellow-600' : 'from-green-500 to-green-600'"
            :style="`width: ${spamScore}%`"
          ></div>
        </div>
      </div>
    </div>

    <!-- Recommendation Box -->
    <div v-if="recommendation" class="bg-gradient-to-br border rounded-2xl p-4 md:p-6 mb-6 md:mb-8 backdrop-blur-xl" :class="recommendationBoxClass">
      <div class="flex flex-col md:flex-row items-start gap-4 md:gap-5">
        <span class="text-4xl md:text-5xl flex-shrink-0">{{ recommendationIcon }}</span>
        <div class="flex-1 min-w-0">
          <p class="font-bold text-lg md:text-xl text-white mb-1.5">{{ recommendation.action }}</p>
          <p class="text-sm md:text-base text-white/80 leading-relaxed">{{ recommendation.reason }}</p>
        </div>
        <div class="flex-shrink-0">
          <span 
            class="inline-block px-3 md:px-4 py-2 rounded-full text-xs md:text-sm font-bold uppercase tracking-wider whitespace-nowrap"
            :class="recommendationBadgeClass"
          >
            {{ recommendation.level }}
          </span>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex flex-wrap gap-2 md:gap-3">
      <button v-if="recommendation && recommendation.action === 'BLOCK'" @click="handleBlock" class="px-4 md:px-6 py-2.5 md:py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 text-sm md:text-base shadow-lg hover:shadow-red-500/30">
        🚫 Block
      </button>
      <button v-if="recommendation && recommendation.action === 'VERIFY'" @click="handleVerify" class="px-4 md:px-6 py-2.5 md:py-3 bg-gradient-to-r from-yellow-600 to-yellow-700 hover:from-yellow-700 hover:to-yellow-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 text-sm md:text-base shadow-lg hover:shadow-yellow-500/30">
        ⚠️ Verify
      </button>
      <button v-if="recommendation && recommendation.action === 'QUARANTINE'" @click="handleQuarantine" class="px-4 md:px-6 py-2.5 md:py-3 bg-gradient-to-r from-orange-600 to-orange-700 hover:from-orange-700 hover:to-orange-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 text-sm md:text-base shadow-lg hover:shadow-orange-500/30">
        📬 Quarantine
      </button>
      <button v-if="recommendation && recommendation.action === 'REVIEW'" @click="handleReview" class="px-4 md:px-6 py-2.5 md:py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 text-sm md:text-base shadow-lg hover:shadow-green-500/30">
        🔍 Review
      </button>
      <button @click="handleCopy" class="px-4 md:px-6 py-2.5 md:py-3 bg-gradient-to-r from-slate-700 to-slate-800 hover:from-slate-600 hover:to-slate-700 text-slate-100 font-bold rounded-xl transition-all transform hover:scale-105 text-sm md:text-base shadow-lg">
        📋 {{ copyMessage || 'Copy Report' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  score: Number,
  spamScore: Number,
  classification: String,
  recommendation: Object,
  metadata: Object
})

const copyMessage = ref('')

// Button handlers
const handleVerify = () => {
  alert(`⚠️ VERIFY ACTION\n\nTo verify this email:\n\n1. DO NOT click any links in the email\n2. Call the sender directly using a known phone number\n3. Confirm they actually sent this email\n\nSender: ${props.metadata?.sender || 'Unknown'}\nSubject: ${props.metadata?.subject || 'Unknown'}\n\nIf they deny sending it → DELETE the email (it's phishing)\nIf they confirm → It's likely legitimate`)
}

const handleBlock = () => {
  alert(`🚫 BLOCK ACTION\n\nThis email should be:\n\n1. Deleted immediately\n2. Sender added to blocklist\n3. Reported to IT/Security\n\nSender: ${props.metadata?.sender || 'Unknown'}\n\nDo NOT interact with any links or attachments.`)
}

const handleQuarantine = () => {
  alert(`📬 QUARANTINE ACTION\n\nThis email should be:\n\n1. Moved to Spam/Junk folder\n2. Reviewed by IT before opening\n3. Analyzed with antivirus if attachment present\n\nSender: ${props.metadata?.sender || 'Unknown'}\n\nWait for IT clearance before opening.`)
}

const handleReview = () => {
  alert(`🔍 REVIEW ACTION\n\nThis email needs careful review:\n\n1. Check sender legitimacy out-of-band\n2. Verify any requests with known contacts\n3. Don't click links until confirmed safe\n\nSender: ${props.metadata?.sender || 'Unknown'}\n\nIf unsure, contact IT/Security.`)
}

const handleCopy = async () => {
  const analysisText = `VAMS Email Security Analysis Report\n\n` +
    `Classification: ${props.classification}\n` +
    `Phishing Score: ${props.score}/100\n` +
    `Spam Score: ${props.spamScore}/100\n` +
    `Recommendation: ${props.recommendation?.action || 'N/A'}\n` +
    `Reason: ${props.recommendation?.reason || 'N/A'}\n\n` +
    `Sender: ${props.metadata?.sender || 'Unknown'}\n` +
    `Subject: ${props.metadata?.subject || 'Unknown'}\n` +
    `Attachments: ${props.metadata?.attachment_count || 0}\n\n` +
    `Analysis Date: ${new Date().toLocaleString()}`

  try {
    await navigator.clipboard.writeText(analysisText)
    copyMessage.value = '✓ Copied to clipboard!'
    setTimeout(() => {
      copyMessage.value = ''
    }, 2000)
  } catch (err) {
    alert('Failed to copy to clipboard')
  }
}

// Determine risk level from classification
const phishingLevel = computed(() => {
  if (props.score >= 70) return 'CRITICAL'
  if (props.score >= 50) return 'HIGH'
  if (props.score >= 30) return 'MEDIUM'
  if (props.score >= 10) return 'LOW'
  return 'MINIMAL'
})

const spamLevel = computed(() => {
  if (props.spamScore >= 80) return 'LIKELY'
  if (props.spamScore >= 50) return 'SUSPICIOUS'
  if (props.spamScore >= 30) return 'LOW'
  return 'NONE'
})

// Color classes
const getPhishingColor = computed(() => {
  if (props.score >= 70) return 'text-red-400'
  if (props.score >= 50) return 'text-orange-400'
  if (props.score >= 30) return 'text-yellow-400'
  return 'text-green-400'
})

const getSpamColor = computed(() => {
  if (props.spamScore >= 80) return 'text-red-400'
  if (props.spamScore >= 50) return 'text-orange-400'
  if (props.spamScore >= 30) return 'text-yellow-400'
  return 'text-green-400'
})

const getPhishingLevel = computed(() => {
  if (props.score >= 70) return 'text-red-400 font-bold'
  if (props.score >= 50) return 'text-orange-400 font-bold'
  if (props.score >= 30) return 'text-yellow-400'
  return 'text-green-400'
})

const getSpamLevel = computed(() => {
  if (props.spamScore >= 80) return 'text-red-400 font-bold'
  if (props.spamScore >= 50) return 'text-orange-400 font-bold'
  if (props.spamScore >= 30) return 'text-yellow-400'
  return 'text-green-400'
})

// Risk classes
const riskClasses = computed(() => {
  const score = Math.max(props.score, props.spamScore)
  if (score >= 70) return 'border-red-500/50 bg-gradient-to-br from-red-900/20 to-red-800/10'
  if (score >= 50) return 'border-orange-500/50 bg-gradient-to-br from-orange-900/20 to-orange-800/10'
  if (score >= 30) return 'border-yellow-500/50 bg-gradient-to-br from-yellow-900/20 to-yellow-800/10'
  return 'border-green-500/50 bg-gradient-to-br from-green-900/20 to-green-800/10'
})

const textColorClass = computed(() => {
  const score = Math.max(props.score, props.spamScore)
  if (score >= 70) return 'text-red-300'
  if (score >= 50) return 'text-orange-300'
  if (score >= 30) return 'text-yellow-300'
  return 'text-green-300'
})

const subtextColorClass = computed(() => {
  const score = Math.max(props.score, props.spamScore)
  if (score >= 70) return 'text-red-200/70'
  if (score >= 50) return 'text-orange-200/70'
  if (score >= 30) return 'text-yellow-200/70'
  return 'text-green-200/70'
})

const riskIcon = computed(() => {
  const score = Math.max(props.score, props.spamScore)
  if (score >= 70) return '🚨'
  if (score >= 50) return '⚠️'
  if (score >= 30) return '⚡'
  return '✅'
})

const classificationDescription = computed(() => {
  const descriptions = {
    'MALICIOUS_PHISHING': 'High confidence phishing attempt - do not interact',
    'SUSPICIOUS_PHISHING': 'Phishing indicators detected - verify sender',
    'LIKELY_SPAM': 'Probable unsolicited marketing or spam',
    'SUSPICIOUS_SPAM': 'May be spam - review before trusting',
    'LEGITIMATE': 'No significant security concerns detected'
  }
  return descriptions[props.classification] || 'Analysis complete'
})

const recommendationIcon = computed(() => {
  if (!props.recommendation) return '📋'
  const actionIcons = {
    'BLOCK': '🚫',
    'VERIFY': '⚠️',
    'QUARANTINE': '📬',
    'REVIEW': '🔍',
    'ACCEPT': '✅'
  }
  return actionIcons[props.recommendation.action] || '📋'
})

const recommendationBadgeClass = computed(() => {
  if (!props.recommendation) return 'bg-blue-500/30 text-blue-200'
  const badgeClasses = {
    'CRITICAL': 'bg-red-500/30 text-red-200',
    'HIGH': 'bg-orange-500/30 text-orange-200',
    'MEDIUM': 'bg-yellow-500/30 text-yellow-200',
    'LOW': 'bg-blue-500/30 text-blue-200'
  }
  return badgeClasses[props.recommendation.level] || 'bg-slate-500/30 text-slate-200'
})
</script>

<style scoped>
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
