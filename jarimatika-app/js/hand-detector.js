// Using MediaPipe Hands directly without CDN issues
class HandDetector {
    constructor() {
        this.model = null;
        this.isLoaded = false;
        this.landmarks = null;
        
        // Finger tip indices
        this.THUMB_TIP = 4;
        this.INDEX_TIP = 8;
        this.MIDDLE_TIP = 12;
        this.RING_TIP = 16;
        this.PINKY_TIP = 20;
        
        // Finger base indices
        this.THUMB_BASE = 2;
        this.INDEX_BASE = 5;
        this.MIDDLE_BASE = 9;
        this.RING_BASE = 13;
        this.PINKY_BASE = 17;
    }

    async loadModel() {
        try {
            // Load MediaPipe Hands model
            const hands = new Hands({
                locateFile: (file) => {
                    return `https