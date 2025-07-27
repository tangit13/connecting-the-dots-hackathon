# Connecting the Dots Hackathon Submission

## How to Run

### Round 1A:
```bash
docker build -f Dockerfile.round1a -t round1a-outline .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1a-outline
```

### Round 1B:
```bash
docker build -f Dockerfile.round1b -t round1b-ranker .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1b-ranker
```

Place PDF files in the `input/` folder and retrieve output JSON from `output/`.