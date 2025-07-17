<template>
  <div class="flex flex-col g-1rem">
    <canvas
      ref="canvas"
      width="280" height="280"
      @pointerdown="startDraw"
      @pointermove="onDraw"
      @pointerup="endDraw"
      @pointerleave="endDraw"
      class="border"
    />
    <div class="flex g-5rem">
      <button @click="clearCanvas" class="p-1 bg-blue-300 mt-2 mb-2 mr-2 text-[20px]">クリア</button>
      <button @click="predict" class="pt-1 pb-1 pr-1 pl-2 bg-green-300 m-2 text-[20px]">GO！</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const emit = defineEmits(['result', 'clear', 'thinking'])

const canvas = ref(null)
let ctx
let drawing = false

onMounted(() => {
  ctx = canvas.value.getContext('2d')
  clearCanvas()
  ctx.strokeStyle = 'white'
  ctx.lineWidth = 10
  ctx.lineCap = 'round'
})

const startDraw = e => {
  drawing = true
  // canvas.setPointerCapture(e.pointerId)
  ctx.beginPath()
  ctx.moveTo(e.offsetX, e.offsetY)
}
const onDraw = e => {
  if (drawing) {
    ctx.lineTo(e.offsetX, e.offsetY)
    ctx.stroke()
  }
}
const endDraw = e => {
  drawing = false
  // canvas.releasePointerCapture(e.pointerId)
}

const clearCanvas = () => {
  // 黒背景でキャンバス全体をクリア
  ctx.fillStyle = 'black'
  ctx.fillRect(0, 0, canvas.value.width, canvas.value.height)
  emit('clear')
}

const predict = async () => {
  const dataUrl = canvas.value.toDataURL('image/png')
  try {
    const { data } = await axios.post('https://mnist-recognition.onrender.com/predict', { image: dataUrl })
    emit('thinking', true); console.log('→ true emitted')
    emit('result', { digits: data.digits, probs: data.probs })

    setTimeout(function () {
      emit('thinking', false);; console.log('→ false emitted')
    }, 7500);

    } catch (error) {
    console.error(error)
    alert('予測に失敗しました')
  } finally {
    // emit('thinking', false)
    // clearCanvas()
  }
}
</script>

<style scoped>
.canvas-container { display: flex; gap: 1rem; }
canvas.border { border: 1px solid #ccc; cursor: crosshair; }
.controls { display: flex; flex-direction: column; gap: .5rem; }

canvas.draw-area {
  touch-action: none;
  -ms-touch-action: none;
}
</style>
