import praw, time
import networkx as nx
from collections import Counter

def process_comment(comment, recursive_link=True):
    '''
    Get the structure of the comment 
    and returns the Nodes and Edges 
    that forms from users interactions 
    represented by the comments tree.
    '''
    
    # if input is not a Comment Type
    if not hasattr(comment,'author'):
        return set(),set()

    # check is there is a user from this post
    if not comment.author:
        # if there are replies, just skip this comment
        if len(comment.replies)>0 and recursive_link:
            nds = set()
            edgs = set()
            for r in list(comment.replies):
                n, e = process_comment(r)
                nds.update(n)
                edgs.update(e)
            return nds, edgs
        else: # otherwise return empty sets
            return set(), set()

    if len(comment.replies) < 1 or not recursive_link:
        return set([comment.author.name]), set()
    
    redditor = comment.author.name
    nodes = set([redditor])
    edges = set()
    for reply in list(comment.replies):
        rnodes, redges = process_comment(reply)
        nodes.update(rnodes)
        edges.update(redges)
        for n in rnodes:
            if not n == redditor:
                edges.add((n, redditor))

    return nodes, edges

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()


'''
------ Main script starts here ------
'''

POST_BY_SUBREDDIT = 500
subreddits_list = ['ManjaroLinux','linuxmint','Ubuntu','fedora','linux','linuxmasterrace']
filename = 'simpledistros'
subcomments_accepted = False

nodes = set()
edges = set()
edges_label = {}

# Login to Reddit
reddit = praw.Reddit(client_id='XXXXXXX', 
        client_secret='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        user_agent='networks_script')

start = time.time()
# Iterate over all the scoped subreddits
for sub_name in subreddits_list:
    subreddit = reddit.subreddit(sub_name)
    
    print('Checking subreddit '+sub_name)
    
    i = 1
    # get iterate through some posts
    for submission in subreddit.hot(limit=POST_BY_SUBREDDIT):
         
        printProgressBar(i,POST_BY_SUBREDDIT, prefix='subreddit')
        i+=1

        # check if the poster exists
        if not submission.author: 
            continue

        comments = list(submission.comments)
        for com in comments:
            cnodes, cedges = process_comment(com,subcomments_accepted)
            author = submission.author.name
            
            # add a interaction with all the comments
            # in the post and the author of the post
            for n in cnodes:
                if not n == author:
                    cedges.add((n,author))
            cnodes.add(author)

            # Add label to edges
            for e in cedges:
                edges_label[e] = sub_name

            # update nodes and edges
            nodes.update(cnodes)
            edges.update(cedges)

end = time.time() - start

print('Parsing finished after {}s, with {} nodes and {} edges'.format(end, len(nodes), len(edges)))

G = nx.Graph()
G.add_nodes_from(list(nodes))
G.add_edges_from(list(edges))

# set edges labels
for k in list(edges_label):
    temp = edges_label[k]
    G.edges[k[0], k[1]]['label'] = temp

# set label of nodes
for n in G:
    labels = []
    for nbr in G[n]:
        labels.append(G.edges[n, nbr]['label'])
    c = Counter(labels)
    most_common = c.most_common()
    if len(most_common) >0:
        G.node[n]['sub'] = most_common[0][0]

# Get only the largest connected sub-graph
G = max(nx.connected_component_subgraphs(G), key=len)

nx.write_pajek(G, filename+'.net')
nx.write_gml(G,filename+'.gml')
print('Finished')
