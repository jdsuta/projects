function MyForm({ userid, load }) {
    const [content, setContent] = React.useState("");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); // put the tag in tbe meta in layout.html

    const handleSubmit = (event) => {
        event.preventDefault(); // To avoid reloading the complete page
        fetch('/savepost', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                userid: userid,
                content: content
            })
        })
            .then(response => response.json())
            .then(result => {
                // console.log(result)
                // evaluates if result.success is true
                if (result.success) {
                    setContent(""); // Clears the form after submit
                    load(0, userid, 1);// Calls the load function to refresh posts with the new post.
                } else {
                    console.error('Post submission failed');
                }
            })
            .catch(error => console.error('Error:', error));
    };

    return (
        <div className="container" id="compose-post">
            <div className="card">
                <div className="card-body">
                    <h3>New Post</h3>
                    <form onSubmit={handleSubmit}>
                        <textarea maxLength="300" className="form-control" placeholder="Content" value={content} onChange={e => setContent(e.target.value)}></textarea>
                        <br />
                        <button type="submit" className="btn btn-primary">Post</button>
                    </form>
                    <br />
                </div>
            </div>
        </div>
    );
}

function Post({ posts, load, Profile, userid, page_number, num_pages, has_next, has_previous, next_page_number, previous_page_number, editpost, Clickededitpost, editPostId, content, updatav, likeUnlike, isLoggedIn }) {
    React.useEffect(() => {
        load(0, userid, page_number);
    }, []); // To just do the action once

    console.log(has_next)

    const [content2, setContent2] = React.useState("");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); // put the tag in tbe meta in layout.html

    const handleSubmit = (event) => {
        event.preventDefault(); // To avoid reloading the complete page
        fetch('/edit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                userid: userid,
                content: content2,
                postid: editPostId
            })
        })
            .then(response => response.json())
            .then(result => {
                // console.log(result)
                // evaluates if result.success is true
                if (result.success) {
                    setContent2(""); // Clears the variable after submit
                    load(0, userid, page_number);// Calls the load function to refresh posts with the new post.
                    updatav();
                } else {
                    console.error('Post submission failed');
                }
            })
            .catch(error => console.error('Error:', error));
    };


    return (
        <div className="container" id="allposts">
            <br />
            <h3>All Posts</h3>

            {posts.map((post, index) => (
                <div className="card">
                    <div className="card-body" key={index}>
                        <div className="row">
                            <div className="col">
                                <h4><a id="link-profile" onClick={() => Profile(post.poster__id, post.poster__username, userid, page_number)}> {post.poster__username}</a></h4>
                            </div>
                            <div className="col text-right">
                                {post.poster__id.toString() === userid ?
                                    <a className="card-text small" onClick={() => editpost(post.id, userid)}>Edit</a>
                                    : null
                                }

                            </div>
                        </div>

                        {Clickededitpost && editPostId === post.id ? (
                            <form onSubmit={handleSubmit}>
                                <textarea
                                    maxLength="300"
                                    className="form-control"
                                    defaultValue={content}
                                    onChange={e => setContent2(e.target.value)}
                                ></textarea>
                                <br />
                                <button type="submit" className="btn btn-primary">Save Edited Post</button>
                                <br />
                                <br />
                            </form>

                        ) : (
                            <p>{post.content}</p>
                        )}



                        {/* Two colums. To have the likes and the date of creation on the same line */}
                        <div className="row">
                            <div className="col">
                                <p className="card-text small">
                                    {isLoggedIn ? (
                                        <a href="javascript:void(0)"
                                            onClick={() => {
                                                likeUnlike(post.id, userid, post.liked)
                                                    .then(() => {
                                                        load(0, userid, page_number);  // Call another function after likeUnlike
                                                    })
                                                    .catch(error => {
                                                        console.error('Error in likeUnlike function:', error);
                                                    });
                                            }}
                                        >
                                            {post.liked ? (<i className="bi bi-heart-fill"></i>)
                                                :
                                                (<i className="bi bi-heart"></i>)}
                                        </a>)

                                        :

                                        (<i className="bi bi-heart"></i>)
                                    }
                                    <span>{" "} {post.like_count}</span>
                                </p>
                            </div>
                            <div className="col text-right">
                                <p className="card-text text-muted small">Posted on: {new Date(post.created_at).toLocaleString()}</p>
                            </div>
                        </div>
                    </div>
                </div >
            ))
            }

            {/* paginator using bootstrap */}
            <br></br>
            <nav aria-label="Page navigation posts">
                <ul className="pagination justify-content-center">
                    {has_previous ?
                        <>
                            <li className="page-item">
                                <a className="page-link" href="javascript:void(0)" onClick={() => load(0, userid, 1)} aria-label="Previous">
                                    <span aria-hidden="true">&laquo;</span>
                                </a>
                            </li>
                            <li className="page-item"><a className="page-link" href="javascript:void(0)" onClick={() => load(0, userid, previous_page_number)}>{previous_page_number}</a></li>
                        </>
                        : null}

                    <li className="page-item active"><a className="page-link" href="javascript:void(0)" onClick={() => load(0, userid, page_number)}>{page_number} <span className="sr-only">(current)</span></a></li>


                    {has_next ?
                        <>
                            <li className="page-item"><a className="page-link" href="javascript:void(0)" onClick={() => load(0, userid, next_page_number)}>{next_page_number}</a></li>
                            <li className="page-item">
                                <a className="page-link" href="javascript:void(0)" onClick={() => load(0, userid, num_pages)} aria-label="Next">
                                    <span aria-hidden="true">&raquo;</span>
                                </a>
                            </li>
                        </>
                        : null}
                </ul>
            </nav>
            <br></br>
            <p className="card-text text-right text-muted small">Page {page_number} of {num_pages}</p>
        </div >
    );
}



function UserProfile({ profiles, followers, following, username, Profile, isLoggedIn, userid, posterid, followed, followUnfollow, page_number, num_pages, has_next, has_previous, next_page_number, previous_page_number, editpost, Clickededitpost, editPostId, content, updatav, likeUnlike }) {


    const [content2, setContent2] = React.useState("");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); // put the tag in tbe meta in layout.html

    const handleSubmit = (event) => {
        event.preventDefault(); // To avoid reloading the complete page
        fetch('/edit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                userid: userid,
                content: content2,
                postid: editPostId
            })
        })
            .then(response => response.json())
            .then(result => {
                // console.log(result)
                // evaluates if result.success is true
                if (result.success) {
                    setContent2(""); // Clears the variable after submit
                    Profile(posterid, username, userid, page_number);// Calls the load function to refresh posts with the new post.
                    updatav();
                } else {
                    console.error('Post submission failed');
                }
            })
            .catch(error => console.error('Error:', error));
    };


    return (
        <div className="container" id="profileposts">
            <br />
            <h3> Profile: {username}</h3>
            <p className="card-text">
                <strong>{followers}</strong> followers
                &ensp;
                <strong>{following}</strong> following
            </p>
            {/* Just for logged in users they have the option to follow or unfollow button */}

            {isLoggedIn ? (
                <>
                    {userid === posterid.toString() ? null :
                        <>
                            {/* comparing if user is followed or unfollowed byt the logged in user. 
                        if followed === 0 it means the user is not following. Therefore, it will show the follow button. If followed it will show the unfollow button */}
                            {followed === 0 ? <button onClick={() => followUnfollow(posterid, userid, followed, username, page_number)} className="btn btn-primary btn-sm">Follow</button> :
                                <button onClick={() => followUnfollow(posterid, userid, followed, username, page_number)} className="btn btn-secondary btn-sm active">Unfollow</button>
                            }
                        </>
                    }
                </>
            ) : null}

            <br />
            <br />

            {profiles.map((profile, index) => (
                <div className="card" key={index}>
                    <div className="card-body">
                        <div className="row">
                            <div className="col">
                                <h4>
                                    <a id="link-profile" onClick={() => { Profile(profile.poster__id, profile.poster__username, userid, page_number); }}>
                                        {profile.poster__username}
                                    </a>
                                </h4>
                            </div>
                            <div className="col text-right">
                                {profile.poster__id.toString() === userid ?
                                    <a className="card-text small" onClick={() => editpost(profile.id, userid)}>Edit</a>
                                    : null
                                }
                            </div>
                        </div>


                        {Clickededitpost && editPostId === profile.id ? (
                            <form onSubmit={handleSubmit}>
                                <textarea
                                    maxLength="300"
                                    className="form-control"
                                    defaultValue={content}
                                    onChange={e => setContent2(e.target.value)}
                                ></textarea>
                                <br />
                                <button type="submit" className="btn btn-primary">Save Edited Post</button>
                                <br />
                                <br />
                            </form>

                        ) : (
                            <p>{profile.content}</p>
                        )}

                        <div className="row">
                            <div className="col">
                                <p className="card-text small">

                                    {isLoggedIn ? (
                                        <a href="javascript:void(0)"
                                            onClick={() => {
                                                likeUnlike(profile.id, userid, profile.liked)
                                                    .then(() => {
                                                        Profile(profile.poster__id, username, userid, page_number);  // Call another function after likeUnlike
                                                    })
                                                    .catch(error => {
                                                        console.error('Error in likeUnlike function:', error);
                                                    });
                                            }}
                                        >
                                            {profile.liked ? (<i className="bi bi-heart-fill"></i>)
                                                :
                                                (<i className="bi bi-heart"></i>)}
                                        </a>)

                                        :

                                        (<i className="bi bi-heart"></i>)}

                                    <span>{" "} {profile.like_count}</span>
                                </p>
                            </div>
                            <div className="col text-right">
                                <p className="card-text text-muted small">Posted on: {new Date(profile.created_at).toLocaleString()}</p>
                            </div>
                        </div>
                    </div>
                </div>
            ))
            }


            {/* paginator using bootstrap */}
            <br></br>
            <nav aria-label="Page navigation example">
                <ul className="pagination justify-content-center">
                    {has_previous ?
                        <>
                            <li className="page-item">
                                {/* Profile(post.poster__id, post.poster__username, userid, page_number) */}
                                <a className="page-link" href="javascript:void(0)" onClick={() => Profile(posterid, username, userid, 1)} aria-label="Previous">
                                    <span aria-hidden="true">&laquo;</span>
                                </a>
                            </li>
                            <li className="page-item"><a className="page-link" href="javascript:void(0)" onClick={() => Profile(posterid, username, userid, previous_page_number)}>{previous_page_number}</a></li>
                        </>
                        : null}

                    <li className="page-item active"><a className="page-link" href="javascript:void(0)" onClick={() => Profile(posterid, username, userid, page_number)}>{page_number} <span className="sr-only">(current)</span></a></li>


                    {has_next ?
                        <>
                            <li className="page-item"><a className="page-link" href="javascript:void(0)" onClick={() => Profile(posterid, username, userid, next_page_number)}>{next_page_number}</a></li>
                            <li className="page-item">
                                <a className="page-link" href="javascript:void(0)" onClick={() => Profile(posterid, username, userid, num_pages)} aria-label="Next">
                                    <span aria-hidden="true">&raquo;</span>
                                </a>
                            </li>
                        </>
                        : null}
                </ul>
            </nav>
            <br></br>
            <p className="card-text text-right text-muted small">Page {page_number} of {num_pages}</p>
        </div>
    );
}


function Following({ posts, load, Profile, userid, page_number, num_pages, has_next, has_previous, next_page_number, previous_page_number, likeUnlike, isLoggedIn }) {
    React.useEffect(() => {
        load(1, userid, page_number);
    }, []); // To just do the action once

    return (
        <div className="container" id="Followingposts">
            <br />
            <h3> Following Posts</h3>

            {posts.map((post, index) => (
                <div className="card">
                    <div className="card-body" key={index}>
                        <div className="row">
                            <div className="col">
                                <h4><a id="link-profile" onClick={() => Profile(post.poster__id, post.poster__username, userid, page_number)}> {post.poster__username}</a></h4>
                            </div>
                            <div className="col text-right">
                                {/* no edit in following since is not neccesary because a user cannot follow itself */}
                                <p className="card-text text-muted small"></p>
                            </div>
                        </div>
                        <p>{post.content}</p>
                        {/* Two colums. To have the likes and the date of creation on the same line */}
                        <div className="row">
                            <div className="col">
                                <p className="card-text small">
                                    {isLoggedIn ? (
                                        <a href="javascript:void(0)"
                                            onClick={() => {
                                                likeUnlike(post.id, userid, post.liked)
                                                    .then(() => {
                                                        load(1, userid, page_number);  // Call another function after likeUnlike
                                                    })
                                                    .catch(error => {
                                                        console.error('Error in likeUnlike function:', error);
                                                    });
                                            }}
                                        >
                                            {post.liked ? (<i className="bi bi-heart-fill"></i>)
                                                :
                                                (<i className="bi bi-heart"></i>)}
                                        </a>)

                                        :

                                        (<i className="bi bi-heart"></i>)
                                    }
                                    <span>{" "} {post.like_count}</span>
                                </p>
                            </div>
                            <div className="col text-right">
                                <p className="card-text text-muted small">Posted on: {new Date(post.created_at).toLocaleString()}</p>
                            </div>
                        </div>
                    </div>
                </div>
            ))}

            {/* paginator using bootstrap */}
            <br></br>
            <nav aria-label="Page navigation example">
                <ul className="pagination justify-content-center">
                    {has_previous ?
                        <>
                            <li className="page-item">
                                <a className="page-link" href="javascript:void(0)" onClick={() => load(1, userid, 1)} aria-label="Previous">
                                    <span aria-hidden="true">&laquo;</span>
                                </a>
                            </li>
                            <li className="page-item"><a className="page-link" href="javascript:void(0)" onClick={() => load(1, userid, previous_page_number)}>{previous_page_number}</a></li>
                        </>
                        : null}

                    <li className="page-item active"><a className="page-link" href="javascript:void(0)" onClick={() => load(1, userid, page_number)}>{page_number} <span className="sr-only">(current)</span></a></li>


                    {has_next ?
                        <>
                            <li className="page-item"><a className="page-link" href="javascript:void(0)" onClick={() => load(1, userid, next_page_number)}>{next_page_number}</a></li>
                            <li className="page-item">
                                <a className="page-link" href="javascript:void(0)" onClick={() => load(1, userid, num_pages)} aria-label="Next">
                                    <span aria-hidden="true">&raquo;</span>
                                </a>
                            </li>
                        </>
                        : null}
                </ul>
            </nav>
            <br></br>
            <p className="card-text text-right text-muted small">Page {page_number} of {num_pages}</p>
        </div>
    );
}



function ParentComponent() {

    const [isLoggedIn, setIsLoggedIn] = React.useState(false);
    const [showChildren, setShowChildren] = React.useState(true);
    const [username, setusername] = React.useState();
    const [posterid, setPosterid] = React.useState();
    const [followers, setFollowers] = React.useState();
    const [following, setFollowing] = React.useState();
    const [profiles, setProfiles] = React.useState([]);
    const [posts, setPosts] = React.useState([]);
    const formElement = document.querySelector("#form");
    const userid = formElement ? formElement.getAttribute('data-userid') : null;
    const [followed, setFollowed] = React.useState();
    const [Clickedollowing, setClickedfollowing] = React.useState(false);

    const [Clickededitpost, setClickededitpost] = React.useState(false);
    const [editPostId, setEditPostId] = React.useState();
    const [content, setContent] = React.useState("");

    const [page_number, setpage_number] = React.useState(1);
    const [num_pages, setnum_pages] = React.useState();
    const [has_next, sethas_next] = React.useState(false);
    const [has_previous, sethas_previous] = React.useState(false);
    const [next_page_number, setnext_page_number] = React.useState();
    const [previous_page_number, setprevious_page_number] = React.useState();

    const [liked, setliked] = React.useState();



    // const [followingflag, setFollowingflag] = React.useState(0);

    React.useEffect(() => {
        const handleClick = () => {
            // Load following
            console.log(`Loading following was clicked`);
            setClickedfollowing(true)
        };

        // Element query selector for button following 
        const followingButton = document.querySelector('#following');
        if (followingButton) {
            followingButton.addEventListener('click', handleClick);
        }

        // Remove the event listener. Necessary to avoid memory leak 
        return () => {
            if (followingButton) {
                followingButton.removeEventListener('click', handleClick);
            }
        };
    }, []);


    const load = (followingflag, userid, page_number) => {
        fetch(`/posts?page_number=${page_number}&followingflag=${followingflag}&userid=${userid}`) // Adjust this URL according to your API endpoint
            .then(response => response.json())
            .then(data => {
                console.log(data); // See what the API returns
                setPosts(data.page_obj);
                setpage_number(data.page_number);
                setnum_pages(data.num_pages);
                sethas_next(data.has_next);
                sethas_previous(data.has_previous);
                setnext_page_number(data.next_page_number);
                setprevious_page_number(data.previous_page_number);
            });
    };


    const Profile = (id, username, userid, page_number) => {
        fetch(`/profile?page_number=${page_number}&profileid=${id}&userid=${userid}`)
            .then(response => response.json())
            .then(data => {
                console.log(data); // Print result
                setProfiles(data.posts);
                setFollowers(data.followers);
                setFollowing(data.following);
                setFollowed(data.followed);
                setpage_number(data.page_number);
                setnum_pages(data.num_pages);
                sethas_next(data.has_next);
                sethas_previous(data.has_previous);
                setnext_page_number(data.next_page_number);
                setprevious_page_number(data.previous_page_number);
                //  Cannot print because is an Async function
            });
        setusername(username);
        setPosterid(id);
        setShowChildren(false);
        setClickedfollowing(false);
    }

    const followUnfollow = (id, userid, followed, username, page_number) => {
        fetch(`/followunfollow?profileid=${id}&userid=${userid}&followed=${followed}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                Profile(id, username, userid, page_number); // Print result
                //  Cannot print because is an Async function
            });
        setShowChildren(false);
    }

    // Have to return because we are calling other functions afterwards
    const likeUnlike = (id, userid, liked) => {
        return fetch(`/likeunlike?postid=${id}&userid=${userid}&liked=${liked}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                return Promise.resolve();
                // Profile(id, username, userid, page_number); // Print result
                //  Cannot print because is an Async function

            });
        // setShowChildren(false);
    }


    const editpost = (id, userid) => {
        fetch(`/edit?postid=${id}&userid=${userid}`)
            .then(response => response.json())
            .then(data => {
                console.log(data.content);
                setContent(data.content);
            });
        setClickededitpost(true);
        setEditPostId(id);
    }

    const updatav = () => {
        setClickededitpost(false);
        setEditPostId(null);
        setContent(null);
    }


    const checkauth = () => {
        try {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content'); // put the tag in tbe meta in layout.html
            if (csrfToken) {
                // Send token with request to django to check if the user is authenticated
                fetch('/checkauth', {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    }
                })
                    .then(response => response.json())
                    .then(result => {
                        console.log(result); // See what the API returns
                        if (result.message === 'Authenticated') {
                            setIsLoggedIn(true);
                        }
                    });

            }
            else {
                // CSRF token is not availabl = set isLoggedIn to false
                setIsLoggedIn(false);
            }
        } catch (error) {
            console.error('Error checking authentication:', error);
            setIsLoggedIn(false)
        }
    }

    React.useEffect(() => {
        checkauth();
    }, []);


    // Correct conditional rendering
    return (
        <>
            {
                Clickedollowing ? (
                    <Following
                        posts={posts}
                        load={load}
                        Profile={Profile}
                        userid={userid}
                        posterid={posterid}
                        page_number={page_number}
                        num_pages={num_pages}
                        has_next={has_next}
                        has_previous={has_previous}
                        next_page_number={next_page_number}
                        previous_page_number={previous_page_number}
                        likeUnlike={likeUnlike}
                        isLoggedIn={isLoggedIn}
                    />
                ) : (
                    showChildren ? (
                        <>
                            {isLoggedIn ? <MyForm userid={userid} load={load} /> : null}
                            <Post
                                posts={posts}
                                load={load}
                                Profile={Profile}
                                userid={userid}
                                posterid={posterid}
                                page_number={page_number}
                                num_pages={num_pages}
                                has_next={has_next}
                                has_previous={has_previous}
                                next_page_number={next_page_number}
                                previous_page_number={previous_page_number}
                                editpost={editpost}
                                Clickededitpost={Clickededitpost}
                                editPostId={editPostId}
                                content={content}
                                updatav={updatav}
                                likeUnlike={likeUnlike}
                                isLoggedIn={isLoggedIn}
                            />
                        </>
                    ) : (
                        <UserProfile
                            profiles={profiles}
                            followers={followers}
                            following={following}
                            username={username}
                            Profile={Profile}
                            isLoggedIn={isLoggedIn}
                            userid={userid}
                            posterid={posterid}
                            followed={followed}
                            followUnfollow={followUnfollow}
                            page_number={page_number}
                            num_pages={num_pages}
                            has_next={has_next}
                            has_previous={has_previous}
                            next_page_number={next_page_number}
                            previous_page_number={previous_page_number}
                            editpost={editpost}
                            Clickededitpost={Clickededitpost}
                            editPostId={editPostId}
                            content={content}
                            updatav={updatav}
                            likeUnlike={likeUnlike}
                            liked={liked}
                        />
                    )
                )}
        </>
    );
}

const rootElement = document.getElementById('root');
if (rootElement) {
    ReactDOM.render(<ParentComponent />, rootElement);
}