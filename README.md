## MojoQA - This project is still in progress

MojoQA is a RAG (Retrieval Augmented Generation) based LLM application that can answer queries
related to Mojo programming language.

Introduced this year, [Mojo](https://www.modular.com/max/mojo) is a novel programming language that seamlessly merges the strengths of Python syntax with elements of systems programming and metaprogramming, effectively bridging the divide between research and production.

Let's see what LLAMA-2 knows about it!

![Avery_LLAMA2_response.JPG](Avery_LLAMA2_response.JPG)

As you can see the response is not accurate.

Now let's see how Mojo QA bot performs.

![mojo_qa_bot_response.JPG](mojo_qa_bot_response.JPG)

For creating Mojo QA Bot, I have extracted the official Mojo documentation and created a vector store containing 
corresponding embeddings. To answer each query, we retrieve the most similar embeddings and provide it to the LLM as context.
Checkout the high level overview diagram below.
### High level overview


### How to reproduce?

### MojoQA Bot in action

### 