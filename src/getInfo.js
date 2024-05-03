import axios from "axios";

export default function getInfo() {
    const VECTOR_SEARCH_ENDPOINT_URL = "https://dbc-379fb5c9-d79a.cloud.databricks.com/explore/data/netflix/rag_chatbot/title_description_index"
    const indexName = 'netflix.rag_chatbot.title_description_index';
    const query = 'korean drama italians?';
    const numResults = 5;

    const queryUrl = "http:localhost:8080/" + `${VECTOR_SEARCH_ENDPOINT_URL}/search?index_name=${indexName}&query=${query}&num_results=${numResults}`;

    axios.get(queryUrl)
    .then(response => {
        // Extract the relevant information from the response
        const resultData = response.data.result.data_array;
        // Process or display the query results as needed
        console.log(resultData);
    })
    .catch(error => {
        // Handle any errors that occur during the API request
        console.error(error);
    });
}
