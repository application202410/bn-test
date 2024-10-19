
## Installation and Running the Project
TODO


## Approach
The brief (and my conversation) stressed the need to keep this simple, so I'm going to start by getting all the basics done, build and the recommendation algorithm and then see how much time I hacve left to play with it and improve it.

I've divided this into a few key tasks:
- Project setup and basic 'Hello World' run instructions
- General project structure
- Download and parse phase
- Person-Job matching phase
- Output


### Project setup
I've reviewed enough developer tests to know how much I appreciate decent, clear and fuss-free instructions to get the code running. For nice, universal ease the approach I'm going with is:
- devcontainer file for development
- simple Dockerfile for 'production' run
- Docker compose file just to save on running Docker commands: I want this to be a one-command launch.

This feels like a good balance between simplicity of use and setup.

### General project structure
Whilst there's an appeal to showing off here and splitting the project into multiple pieces - e.g. a Recommendation API that ingests data and responds to POST requests for individual people, I think that's probably outside the scope of this task.

Keeping a clear focus on the end goal, I'm going to have:
- A main executable script
- A downloader that does all the outwards requests and parses data
- An interchangeable recommendations engine
    - This will take all the parsed data and returns a map of Person->Jobs.
    - Interchangeable so I can play around with different versions as drop-in replacements.
- A formatter that takes the mapped recommendations and writes output
    - This could e.g. write to a DB, serialise to JSON, etc.
    - But here it will simply print to console.
- Tests
    - I'm not going to work towards 100% coverage, given time constraints but will write tests mainly to help me as I write new code.


 ## Discussion

 > a brief acknowledgement of the challenges posed by the problem and its domain and a discussion of the choices you've made and your reasons.