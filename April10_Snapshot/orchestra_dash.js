class Orchestra {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.instruments = {};

        // --- 1. THE SIGNAL CHAIN (Order Matters!) ---
        // Final Output Safety: Stops digital distortion (clipping)
        this.limiter = new Tone.Limiter(-1).toDestination();

        // Glue: Squeezes the loud peaks so the orchestra sounds "as one"
        this.compressor = new Tone.Compressor({
            threshold: -20,
            ratio: 3,
            attack: 0.03,
            release: 0.1
        }).connect(this.limiter);

        // Space: Gives the strings a hall-like feel
        this.reverb = new Tone.Reverb({
            decay: 2.5,
            preDelay: 0.1,
            wet: 0.3 
        }).connect(this.compressor);
    }

    parseFiles(instrumentType, duration, dynamic) {
        if (!ORCHESTRA_MAPS[instrumentType] || !ORCHESTRA_MAPS[instrumentType][duration]) return {};
        
        const rawData = ORCHESTRA_MAPS[instrumentType][duration];
        const lines = rawData.split('\n');
        const map = {};

        lines.forEach(line => {
            const clean = line.trim();
            if (!clean || !clean.includes(`_${dynamic}_`)) return;
            const parts = clean.split('_');
            if (parts.length > 1) {
                const note = parts[1].replace('s', '#');
                map[note] = clean;
            }
        });
        return map;
    }

    async loadInstrument(type, dynamic = "forte") {
        let finalMap = {};
        const map05 = this.parseFiles(type, "05", dynamic);
        const map1 = this.parseFiles(type, "1", dynamic);
        Object.assign(finalMap, map05, map1); // Merges both, 1s takes priority

        if (this.instruments[type]) {
            this.instruments[type].dispose();
        }

        return new Promise((resolve) => {
            if (Object.keys(finalMap).length === 0) {
                resolve();
                return;
            }
            
            const folderName = type === "bass" ? "double-bass" : type;
            
            // Create Sampler and connect to REVERB (not Destination)
            this.instruments[type] = new Tone.Sampler({
                urls: finalMap,
                baseUrl: `${this.baseUrl}/${folderName}/`,
                // SMOOTHING: Add a tiny attack to prevent clicking/popping
                attack: 0.41,
                release: 0.5, 
                onload: () => {
                    console.log(`${type.toUpperCase()} loaded.`);
                    resolve();
                }
            }).connect(this.reverb); // Sampler -> Reverb -> Compressor -> Limiter -> Speakers
        });
    }

    async loadAll(dynamic = "forte") {
        // Wait for Reverb to generate its impulse response before playing
        await this.reverb.ready;
        await Promise.all([
            this.loadInstrument("violin", dynamic),
            this.loadInstrument("viola", dynamic),
            this.loadInstrument("cello", dynamic),
            this.loadInstrument("bass", dynamic)
        ]);
    }

    play(type, note, length = "8n", velocity = 0.85) {
        if (this.instruments[type] && this.instruments[type].loaded) {
            const clampedVelocity = Math.max(0.05, Math.min(1, velocity));
            this.instruments[type].triggerAttackRelease(note, length, undefined, clampedVelocity);
        }
    }
}
