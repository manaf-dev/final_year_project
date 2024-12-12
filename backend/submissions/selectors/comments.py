from submissions.models.submissions import Comment


def get_comments(submission_id):
    try:
        comments = Comment.objects.filter(submission=submission_id)
        return comments
    except:
        return None
