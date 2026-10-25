// 升降 Key：不改變速度，只改變音高（兩個交錯讀取點的延遲線變調法）
class PitchShifter extends AudioWorkletProcessor {
  static get parameterDescriptors() {
    return [{ name: "semitones", defaultValue: 0, minValue: -12, maxValue: 12, automationRate: "k-rate" }];
  }
  constructor() {
    super();
    this.win = Math.round(sampleRate * 0.07);        // 每一段約 70 毫秒
    this.size = this.win * 2 + 256;
    this.buf = new Float32Array(this.size);
    this.w = 0;
    this.phase = 0;
  }
  read(d) {
    let pos = this.w - d;
    while (pos < 0) pos += this.size;
    const i = Math.floor(pos), f = pos - i;
    const a = this.buf[i % this.size], b = this.buf[(i + 1) % this.size];
    return a + (b - a) * f;
  }
  process(inputs, outputs, params) {
    const inp = inputs[0], out = outputs[0];
    if (!out || !out.length) return true;
    const n = out[0].length;
    const ch0 = inp && inp[0];
    const st = params.semitones[0];
    const ratio = Math.pow(2, st / 12);
    const step = (1 - ratio) / this.win;
    const W = this.win, buf = this.buf, size = this.size;
    const o = out[0];
    for (let k = 0; k < n; k++) {
      // 左右聲道在前面已經合成同一個聲音，這裡只處理一個再複製
      const x = ch0 ? ch0[k] : 0;
      buf[this.w] = x;
      let y;
      if (st === 0) {
        y = x;
      } else {
        let p1 = this.phase, p2 = p1 + 0.5; if (p2 >= 1) p2 -= 1;
        const g1 = Math.sin(Math.PI * p1) ** 2, g2 = Math.sin(Math.PI * p2) ** 2;
        y = this.read(p1 * W + 1) * g1 + this.read(p2 * W + 1) * g2;
        this.phase += step;
        if (this.phase >= 1) this.phase -= 1; else if (this.phase < 0) this.phase += 1;
      }
      o[k] = y;
      this.w = (this.w + 1) % size;
    }
    for (let c = 1; c < out.length; c++) out[c].set(o);
    return true;
  }
}
registerProcessor("pitch-shifter", PitchShifter);
