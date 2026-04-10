// orchestra.js
const SAMPLE_BASE_URL = "https://your-server.com/samples/"; // Where your mp3s are hosted

const instruments = {
    violin: new Tone.Sampler({
        urls: {
            "G3": "violin_G3_1_forte_arco-normal.mp3",
            "G4": "violin_G4_1_forte_arco-normal.mp3",
            "G5": "violin_G5_1_forte_arco-normal.mp3",
            "G6": "violin_G6_1_forte_arco-normal.mp3"
        },
        baseUrl: SAMPLE_BASE_URL,
        release: 1
    }).toDestination(),

    viola: new Tone.Sampler({
        urls: {
            "C3": "viola_C3_1_piano_arco-normal.mp3",
            "G4": "viola_G4_1_piano_arco-normal.mp3",
            "C5": "viola_C5_1_piano_arco-normal.mp3"
        },
        baseUrl: SAMPLE_BASE_URL
    }).toDestination(),

    cello: new Tone.Sampler({
        urls: {
            "C2": "cello_C2_1_mezzo-piano_arco-normal.mp3",
            "G3": "cello_G3_1_mezzo-piano_arco-normal.mp3",
            "C4": "cello_C4_1_mezzo-piano_arco-normal.mp3"
        },
        baseUrl: SAMPLE_BASE_URL
    }).toDestination(),

    bass: new Tone.Sampler({
        urls: {
            "C1": "double-bass_C1_1_mezzo-piano_arco-normal.mp3",
            "G2": "double-bass_G2_1_mezzo-piano_arco-normal.mp3"
        },
        baseUrl: SAMPLE_BASE_URL
    }).toDestination()
};

// Global play function for the dashboard to call
function playInstrument(type, note, duration = "4n") {
    if (instruments[type]) {
        instruments[type].triggerAttackRelease(note, duration);
    }
}