from flask import Blueprint, render_template, redirect, url_for, flash

from ..forms import CompanyForm, CompanyBranchForm
from ..models import Company, Branch

bp = Blueprint('company', __name__, template_folder='../templates', url_prefix='/company')


@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Displays the company details.
    """
    company_form = CompanyForm(obj=Company.query.first())
    _company = Company.query.first()
    branches = Branch.query.all()
    if company_form.validate_on_submit():
        _company = Company.query.first()
        if not _company:
            _company = Company()
        company_form.populate_obj(_company)
        _company.name = company_form.name.data.title()
        _company.update()
        return redirect(url_for('.index'))
    return render_template('admin/company/index.html', title='Company', company=_company, company_form=company_form,
                           branches=branches)


@bp.route('/branch/<int:branch_id>/edit', methods=['GET', 'POST'])
def edit_branch(branch_id):
    """
    Edits the branch.

    Args:
        branch_id: The branch id.

    Returns:
        The company page.
    """
    _branch = Branch.query.get(branch_id)
    branch_form = CompanyBranchForm(obj=_branch)
    if branch_form.validate_on_submit():
        branch_form.populate_obj(_branch)
        _branch.update()
        return redirect(url_for('.index'))
    return render_template('admin/company/branch.html', title='Edit Branch', branch_form=branch_form, branch=_branch)


@bp.route('/branch/delete/<int:branch_id>')
def delete_branch(branch_id):
    """
    Deletes the branch.

    Args:
        branch_id: The branch id.

    Returns:
        The company page.
    """
    branch = Branch.query.get(branch_id)
    company_branches = Branch.query.filter_by(company_id=branch.company_id).all()
    # If there is more than one branch, delete the branch.
    if len(company_branches) > 1:
        branch.delete()
        flash('Branch deleted successfully.', 'green')
    else:
        flash('You must have at least one active branch.', 'red')
    return redirect(url_for('.index'))


@bp.route('/branch/toggle/<int:branch_id>')
def toggle_branch(branch_id):
    """
    Toggles the branch. (Enables/Disables)

    Args:
        branch_id: The branch id.

    Returns:
        The company page.
    """
    branches = Branch.query.all()
    branch = Branch.query.get(branch_id)
    # If there is more than one branch, toggle the branch.
    if len(branches) > 1:
        branch.toggle()
        flash('Branch toggled successfully.', 'green')
    else:
        flash('You must have at least one active branch.', 'red')
    return redirect(url_for('.index'))
