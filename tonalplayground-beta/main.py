import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
import io
import asyncio
from pyodide.ffi import create_proxy
from js import document, console, Uint8Array, window, File
from js import addEventListener

def generate_waveforms(event):

  chords = [
      ['Octave', '0 0', '8'],
      ['Fifth', '0 7', '5'],
      ['Fifth 9th', '0 7 2', '5add9'],
      ['Major', '0 4 7', 'maj'],
      ['Major 6th', '0 4 7 9', 'maj6'],
      ['Major 7th', '0 4 7 11', 'maj7'],
      ['Major 9th', '0 4 7 11 2', 'maj9'],
      ['Add9', '0 4 7 2', 'add9'],
      ['Minor', '0 3 7', 'm'],
      ['Minor 6th', '0 3 7 9', 'm6'],
      ['Minor 7th', '0 3 7 10', 'm7'],
      ['Minor 9th', '0 3 7 10 2', 'm9'],
      ['Minor 11th', '0 3 7 10 2 5', 'm11'],
      ['Dominant 7th', '0 4 7 10', '7'],
      ['Dominant 9th', '0 4 7 10 2', '9'],
      ['Dominant 11th', '0 4 7 10 2 5', '11'],
      ['Dominant 13th', '0 4 7 10 2 5 9', '13'],
      ['Diminished', '0 3 6', 'dim'], 
      ['Diminished 7th', '0 3 6 9', 'dim7'],
      ['Half-Diminished', '0 3 6 10', 'm7b5'],
      ['Augmented', '0 4 8', 'aug'],
      ['Augmented 7th', '0 4 8 10', 'aug7'],
      ['Suspended 2nd', '0 2 7', 'sus2'],
      ['Suspended 4th', '0 5 7', 'sus4'],
      ['Custom Chord', '', '']
  ]

  chromatic_scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
  chromatic_base_pitches = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87]
  harmonic_ratios = [1/1, 16/15, 9/8, 6/5, 5/4, 4/3, 7/5, 3/2, 8/5, 5/3, 9/5, 15/8]
  adjustments = ['+0.0', '+11.95', '+4.12', '+15.07', '-13.71', '-2.38', '-17.31', '+1.77', '+13.29', '-15.81', '+17.14', '-12.03']
  intervals = ['Tonic', 'Minor 2nd', 'Major 2nd', 'Minor 3rd', 'Major 3rd', 'Perfect 4th', 'Aug 4th / Dim 5th', 'Perfect 5th', 'Minor 6th', 'Major 6th', 'Minor 7th', 'Major 7th']

  chromatic_pitches = [pitch*2**4 for pitch in chromatic_base_pitches]

  chord_type = (document.getElementById("chordSelector").selectedIndex) - 2

  frequencies = []  

  pureIntonation = int(js.pureIntonation)
  root = int(js.root)
  voicing = [int(note) for note in js.voicing]
  
  if pureIntonation == 1:
    for i, scale_index in enumerate(voicing):
      if i != 0 and scale_index <= max(voicing[:i]):
        frequencies.append(chromatic_pitches[root]*2*harmonic_ratios[scale_index])
        voicing[i] = scale_index + 12
      else:
        frequencies.append(chromatic_pitches[root]*harmonic_ratios[scale_index])

  elif pureIntonation == 0:
    for i, scale_index in enumerate(voicing):
      if i != 0 and scale_index <= max(voicing[:i]):
        frequencies.append(chromatic_pitches[(root+scale_index)%12]*2)
        voicing[i] = scale_index + 12
      else:
        if root + scale_index >= 12:
          frequencies.append(chromatic_pitches[(root+scale_index)%12]*2)
        else: 
          frequencies.append(chromatic_pitches[(root+scale_index)])
  js.createObject(create_proxy(frequencies), "frequencies")
  #js.chord_pitches = frequencies
  #print(f'\n{chords[chord_type][0]} | {chromatic_scale[root]}{chords[chord_type][2]}')
  #print([chromatic_scale[((int(i)+root)%len(chromatic_scale))] for i in voicing])
  #print(voicing)

  #print(', '.join(map(str, [round(1200*(math.log((harmonic_ratios[note]*chromatic_pitches[root])/chromatic_pitches[((note+root)%len(chromatic_pitches))])/math.log(2)), 2) for note in voicing])))
  #print(' '.join(map(str, [adjustments[i] for i in voicing])))


  t = np.linspace(0, 10/min(frequencies), int(max(frequencies)*100 * 10/min(frequencies)), endpoint=False)

  colors = ["red", "blue", "green", "magenta", "black", "cyan", "yellow"]

  for freq in enumerate(frequencies):
    plt.figure(figsize=(8, 2))

    y = np.sin(2 * np.pi * freq[1] * t + np.pi/2)

    plt.plot(t, y, color=colors[freq[0]])

    if pureIntonation == 1:
      plt.title(f"{[intervals[((int(i))%len(intervals))] for i in voicing][freq[0]]} | {[chromatic_scale[((int(i)+root)%len(chromatic_scale))] for i in voicing][freq[0]]} | {round(freq[1], 2)}Hz | {adjustments[voicing[freq[0]]%12]} Cents")
    elif pureIntonation == 0:
      plt.title(f"{[intervals[((int(i))%len(intervals))] for i in voicing][freq[0]]} | {[chromatic_scale[((int(i)+root)%len(chromatic_scale))] for i in voicing][freq[0]]} | {round(freq[1], 2)}Hz | +0.0 Cents")
    plt.ylim(-1.1, 1.1)

    plt.yticks([])
    plt.xticks([])
    #plt.grid(True)
    plt.tight_layout()
    

    my_stream = io.BytesIO()
    plt.savefig(my_stream, transparent=True)

    image_file = File.new([Uint8Array.new(my_stream.getvalue())], f"{freq[0]}.png", {type: "image/png"})

    new_image = document.createElement('img')
    new_image.src = window.URL.createObjectURL(image_file)
    document.getElementById(f"{freq[0]}_png").appendChild(new_image)
    plt.close()

  plt.figure(figsize=(8, 2))

  
  for freq in enumerate(frequencies):

    # Create layered plot
    plt.plot(t, np.sin(2 * np.pi * freq[1] * t + np.pi/2), color=colors[freq[0]])

  plt.ylim(-1.1, 1.1)
  plt.title(f'{chromatic_scale[root]} {chords[chord_type][0]} | Layered')
  plt.yticks([])
  plt.xticks([])
  #plt.grid(True)
  plt.tight_layout()

  my_stream = io.BytesIO()
  plt.savefig(my_stream, transparent=True)
  

  image_file = File.new([Uint8Array.new(my_stream.getvalue())], "layered.png", {type: "image/png"})

  new_image = document.createElement('img')
  new_image.src = window.URL.createObjectURL(image_file)
  document.getElementById("layered_png").appendChild(new_image)
  
  plt.close()

  plt.figure(figsize=(8, 2))
  combined_wave = np.zeros_like(t)
  for freq in enumerate(frequencies):
    # Create additive plot
    combined_wave += np.sin(2 * np.pi * freq[1] * t + np.pi/2)
  max_value = np.max(np.abs(combined_wave))
  normalized_wave = combined_wave / max_value if max_value != 0 else combined_wave
  plt.plot(t, normalized_wave, 'black')

  plt.ylim(-1.1, 1.1)
  plt.title(f'{chromatic_scale[root]} {chords[chord_type][0]} | Combined')
  plt.yticks([])
  plt.xticks([])
  #plt.grid(True)
  plt.tight_layout()

  my_stream = io.BytesIO()
  plt.savefig(my_stream, transparent=True)
  

  image_file = File.new([Uint8Array.new(my_stream.getvalue())], "combined.png", {type: "image/png"})

  new_image = document.createElement('img')
  new_image.src = window.URL.createObjectURL(image_file)
  document.getElementById("combined_png").appendChild(new_image)
  
  plt.close()

def setup():
  generate_waveforms_proxy = create_proxy(generate_waveforms)
  #document.getElementById("chordSelector").addEventListener("change", generate_waveforms_proxy)
  #document.getElementById("noteSelector").addEventListener("change", generate_waveforms_proxy)
  document.addEventListener('createChord', generate_waveforms_proxy)
setup()
