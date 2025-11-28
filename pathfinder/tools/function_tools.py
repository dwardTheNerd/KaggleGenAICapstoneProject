def split_text_into_chunks(content, max_chunk_size=1000) -> list[str]:
    """
    Splits text into multiple smaller chunks.

    Args:
        content: This is the string containing the text to be split.
        max_chunk_size: The maximum size of each chunk.

    Returns:
        List of strings, with each string represents a chunk of the broken content.
    """
    words = content.split()
    chunks = []
    current_chunk = []

    current_length = 0
    for word in words:
        # Check if adding this word would exceed the max_chunk_size
        if current_length + len(word) + (1 if current_chunk else 0) > max_chunk_size:
            # Join the current chunk of words and append to list
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + (1 if current_chunk[:-1] else 0)

    # Add any remaining words as last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks