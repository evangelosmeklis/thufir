import { ContextProvider, ContextProviderDescription } from "..";
import { ExtensionIde } from "../../ide";
import { ContextItem } from "../../llm/types";

class FileContextProvider extends ContextProvider {
  static description: ContextProviderDescription = {
    title: "file",
    displayTitle: "Files",
    description: "Type to search",
    dynamic: false,
    requiresQuery: false,
  };

  async getContextItems(query: string): Promise<ContextItem[]> {
    // Assume the query is a filepath
    query = query.trim();
    const content = await new ExtensionIde().readFile(query);
    return [
      {
        name: query.split(/[\\/]/).pop() || query,
        description: query,
        content,
        id: {
          providerTitle: FileContextProvider.description.title,
          itemId: query,
        },
      },
    ];
  }
  async load(): Promise<void> {}
}

export default FileContextProvider;