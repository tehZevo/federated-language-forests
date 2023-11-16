# Federated Language Forests

## POST Methods
*Note: all input/output sequeces should be provided in base64 to support arbitrary byte sequences*

### /begin
* Begins a new "session" and returns a session identifier (any object, but likely just a string)
* Optionally accepts batch size for parallelized consumption/generation
* This would be a great place to initialize the state with a prompt

### /update
* Provide your session identifier and a batch of input sequences
* Updates the internal state of the tree
  * For transformers, this is likely just appending to the current input sequence until the input length is reached, and then discarding old data
  * For RNN, update state
* Updating should, if possible, retain at least one previous state in memory for the session for rollback purposes
* It is also possible for nodes to train or fit automatically when update is called

### /generate
* Accepts a session identifier and an optional minimum number of tokens to generate
* Generate at least the minimum number of tokens requested (or some model-determined default)
  * May generate MORE than the requested number, due to model architecture
* It may be useful to output token probabilities as well for ensemble purposes

### /rollback
* Accepts a session identifier
* Rolls the given session back to the previous update call
* This is useful for truncating output at the end of a sentence/message (e.g. in chatbots)

### /end
* End the session

## Federation
As each node (or "tree") exposes its methods via HTTP POST requests, nodes can use other nodes for training or generation purposes.
For instance, one tree can pull sequences via `generate` and use this output for training data. Another potential use is combining multiple node outputs in an ensemble fashion.

## Producer nodes
* Nodes may choose to implement only `generate`, or perhaps `begin` as well (for session-long generation parameters)

## Example node types
### Wikipedia output node
* Given an article url, title, or query, produce text from a Wikipedia article

### Markov chain generator
* Generate text using a Markov chain

### Ensemble generator
* Calls `generate` on multiple models and then combines their outputs (weighted average, random choice, etc.)
* Such methods may require generating a smaller number of tokens per call, so that outputs can be meaningfully combined

### Prompt/processing nodes
* Prompt nodes could call `begin` on another node and `update` it with a prompt
* Other processing features such as chatbot message truncation and prefixing

## TODO
* Make installable Python package
* Wrap an existing LLM as an FLF tree
* Markov chain example
* File/download/yt-dlp node
* Summarize node (use `begin`/`update` to feed text to be summarized)
* Chatbot node (handles prompting/prefixing)
