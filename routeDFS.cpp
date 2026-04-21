#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <algorithm>
#include <limits>
#include <cctype>
using namespace std;
// Graph: node -> list of (neighbor, distance)
map<string, vector<pair<string, int>>> graph;

// To store all routes: each route is a pair (vector of nodes, total distance)
vector<pair<vector<string>, int>> allRoutes;

/**
 * Recursive DFS to find all simple paths from start to end.
 * 
 * @param current      Current node being visited
 * @param target       Destination node
 * @param path         Current path (list of nodes)
 * @param visited      Set of visited nodes to avoid cycles
 * @param currentDist  Accumulated distance so far
 */
void dfs(const string& current, const string& target,
         vector<string>& path, set<string>& visited, int currentDist) {
    
    if (current == target) {
        // Found a complete route
        allRoutes.push_back({path, currentDist});
        return;
    }
    
    // Explore all neighbors
    for (const auto& neighborPair : graph[current]) {
        string neighbor = neighborPair.first;
        int distance = neighborPair.second;
        
        if (visited.find(neighbor) == visited.end()) {
            // Mark visited and add to path
            visited.insert(neighbor);
            path.push_back(neighbor);
            
            // Recurse
            dfs(neighbor, target, path, visited, currentDist + distance);
            
            // Backtrack
            path.pop_back();
            visited.erase(neighbor);
        }
    }
}

/**
 * Finds all simple routes from start to end using DFS.
 * 
 * @param start Start node
 * @param end   End node
 * @return      Vector of (path, total distance)
 */
vector<pair<vector<string>, int>> findAllRoutes(const string& start, const string& end) {
    allRoutes.clear();
    vector<string> path = {start};
    set<string> visited = {start};
    dfs(start, end, path, visited, 0);
    return allRoutes;
}

/**
 * Recommends the shortest route (minimum total distance).
 * 
 * @param routes List of all routes
 * @return       Pair of (best route, best distance), or empty if none
 */
pair<vector<string>, int> recommendShortestRoute(const vector<pair<vector<string>, int>>& routes) {
    if (routes.empty()) {
        return {{}, numeric_limits<int>::max()};
    }
    
    auto best = min_element(routes.begin(), routes.end(),
        [](const pair<vector<string>, int>& a, const pair<vector<string>, int>& b) {
            return a.second < b.second;
        });
    
    return *best;
}

/**
 * Display all available locations (sorted).
 */
void displayLocations() {
    cout << "\n Available Locations:\n";
    vector<string> locations;
    for (const auto& entry : graph) {
        locations.push_back(entry.first);
    }
    sort(locations.begin(), locations.end());
    for (size_t i = 0; i < locations.size(); ++i) {
        cout << "   " << i+1 << ". " << locations[i] << "\n";
    }
}

/**
 * Convert string to title case (first letter uppercase, rest lowercase) for matching.
 */
string toTitleCase(string str) {
    if (str.empty()) return str;
    transform(str.begin(), str.end(), str.begin(), ::tolower);
    str[0] = toupper(str[0]);
    return str;
}

/**
 * Check if a location exists in the graph.
 */
bool isValidLocation(const string& loc) {
    return graph.find(loc) != graph.end();
}

/**
 * Initialize the graph with predefined locations and distances.
 */
void initGraph() {
    // Undirected weighted graph
    graph["Home"] = {{"Mall", 5}, {"School", 3}};
    graph["Mall"] = {{"Home", 5}, {"Park", 2}, {"Library", 4}};
    graph["School"] = {{"Home", 3}, {"Library", 6}, {"Cafe", 7}};
    graph["Park"] = {{"Mall", 2}, {"Library", 1}, {"Office", 3}};
    graph["Library"] = {{"Mall", 4}, {"School", 6}, {"Park", 1}, {"Office", 2}};
    graph["Cafe"] = {{"School", 7}, {"Office", 5}};
    graph["Office"] = {{"Park", 3}, {"Library", 2}, {"Cafe", 5}};
}

int main() {
    initGraph();
    
    cout << "============================================================\n";
    cout << "   ROUTE RECOMMENDATION SYSTEM using DFS (C++)\n";
    cout << "============================================================\n";
    
    while (true) {
        cout << "\n MENU:\n";
        cout << "1. Find and recommend route\n";
        cout << "2. Show all locations\n";
        cout << "3. Exit\n";
        cout << "Enter your choice (1-3): ";
        
        int choice;
        cin >> choice;
        cin.ignore(); // ignore newline
        
        if (choice == 1) {
            displayLocations();
            
            string start, end;
            cout << "\nEnter START location: ";
            getline(cin, start);
            start = toTitleCase(start);
            
            cout << "Enter DESTINATION location: ";
            getline(cin, end);
            end = toTitleCase(end);
            
            // Validate locations
            if (!isValidLocation(start) || !isValidLocation(end)) {
                cout << "Error: One or both locations not found!\n";
                continue;
            }
            
            if (start == end) {
                cout << " Start and destination are the same! You're already there.\n";
                continue;
            }
            
            cout << "\nSearching for routes from '" << start << "' to '" << end << "'...\n";
            
            auto routes = findAllRoutes(start, end);
            
            if (routes.empty()) {
                cout << "No route found from '" << start << "' to '" << end << "'!\n";
                continue;
            }
            
            cout << "\nFound " << routes.size() << " possible route(s):\n";
            cout << "------------------------------------------------------------\n";
            
            for (size_t i = 0; i < routes.size(); ++i) {
                const auto& route = routes[i].first;
                int dist = routes[i].second;
                cout << "Route " << i+1 << ": ";
                for (size_t j = 0; j < route.size(); ++j) {
                    if (j > 0) cout << " -> ";
                    cout << route[j];
                }
                cout << "\n   Total distance: " << dist << " km\n\n";
            }
            
            auto best = recommendShortestRoute(routes);
            cout << "------------------------------------------------------------\n";
            cout << " RECOMMENDATION \n";
            cout << "Best route: ";
            for (size_t j = 0; j < best.first.size(); ++j) {
                if (j > 0) cout << " ->";
                cout << best.first[j];
            }
            cout << "\nTotal distance: " << best.second << " km\n";
            cout << "============================================================\n";
            
        } else if (choice == 2) {
            displayLocations();
        } else if (choice == 3) {
            cout << "\n Thank you for using the Route Recommendation System!\n";
            break;
        } else {
            cout << " Invalid choice! Please enter 1, 2, or 3.\n";
        }
    }
    
    return 0;
}