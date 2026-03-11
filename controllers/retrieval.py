from services.llm_factory import get_vector_store, get_llm
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


def answer_query(query: str):

    # Connect to vector store
    vector_store = get_vector_store()

    # Retrieve more chunks for better context
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
    )

    # Better prompt
    prompt = ChatPromptTemplate.from_template(
        """
You are an assistant answering questions from a document.

Use ONLY the provided context to answer the question.

If the answer is not present in the context, say:
"I could not find the answer in the document."

Context:
{context}

Question:
{input}

Answer:
"""
    )

    # Load LLM
    llm = get_llm()

    # Build chains
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Run query
    response = retrieval_chain.invoke({"input": query})

    # Debugging (optional but useful)
    print("\n🔎 Retrieved Contexts:\n")
    for doc in response["context"]:
        print(doc.page_content[:200], "\n")

    return {
        "answer": response["answer"],
        "retrieved_contexts": [
            doc.page_content for doc in response["context"]
        ]
    }