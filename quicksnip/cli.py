import click
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from .database import Database
from .models import Snippet

console = Console()
db = Database()


@click.group()
def cli():
    """quicksnip - A fast, terminal-based code snippet manager."""
    pass


@cli.command()
@click.argument("name")
@click.option("--description", "-d", default="", help="Description of the snippet")
@click.option("--language", "-l", default="", help="Programming language")
@click.option("--tags", "-t", default="", help="Comma-separated tags")
@click.option("--code", "-c", default="", help="Code (or use stdin)")
def add(name, description, language, tags, code):
    """Add a new snippet."""
    if not code:
        code = click.get_text_stream("stdin").read()
    if not code.strip():
        console.print("[red]Error: Code cannot be empty[/red]")
        raise SystemExit(1)
    snippet = Snippet(
        id=None,
        name=name,
        description=description,
        language=language,
        code=code,
        tags=[t.strip() for t in tags.split(",") if t.strip()],
    )
    try:
        db.add_snippet(snippet)
        console.print(f"[green]✓[/green] Snippet '{name}' added successfully!")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise SystemExit(1)


@cli.command()
@click.argument("query", required=False, default="")
@click.option("--language", "-l", default="", help="Filter by language")
@click.option("--tag", "-t", default="", help="Filter by tag")
def search(query, language, tag):
    """Search snippets."""
    snippets = db.search_snippets(query, language, tag)
    if not snippets:
        console.print("[yellow]No snippets found.[/yellow]")
        return
    table = Table(title=f"Search Results ({len(snippets)} found)")
    table.add_column("Name", style="cyan")
    table.add_column("Language", style="green")
    table.add_column("Tags", style="yellow")
    table.add_column("Description", style="white")
    for s in snippets:
        table.add_row(
            s.name,
            s.language or "-",
            ", ".join(s.tags) if s.tags else "-",
            s.description[:50] + "..." if len(s.description) > 50 else s.description,
        )
    console.print(table)


@cli.command()
@click.argument("name")
def copy(name):
    """Copy a snippet to clipboard."""
    snippet = db.get_snippet(name)
    if not snippet:
        console.print(f"[red]Snippet '{name}' not found.[/red]")
        raise SystemExit(1)
    pyperclip.copy(snippet.code)
    console.print(f"[green]✓[/green] Copied '{name}' to clipboard!")


@cli.command(name="list")
@click.option("--language", "-l", default="", help="Filter by language")
def list_cmd(language):
    """List all snippets."""
    snippets = db.search_snippets(language=language)
    if not snippets:
        console.print("[yellow]No snippets found.[/yellow]")
        return
    table = Table(title=f"Snippets ({len(snippets)} total)")
    table.add_column("Name", style="cyan")
    table.add_column("Language", style="green")
    table.add_column("Tags", style="yellow")
    table.add_column("Description", style="white")
    for s in snippets:
        table.add_row(
            s.name,
            s.language or "-",
            ", ".join(s.tags) if s.tags else "-",
            s.description[:50] + "..." if len(s.description) > 50 else s.description,
        )
    console.print(table)


@cli.command()
@click.argument("name")
def delete(name):
    """Delete a snippet."""
    if db.delete_snippet(name):
        console.print(f"[green]✓[/green] Snippet '{name}' deleted!")
    else:
        console.print(f"[red]Snippet '{name}' not found.[/red]")
        raise SystemExit(1)


@cli.command()
@click.argument("name")
def show(name):
    """Show a snippet with syntax highlighting."""
    snippet = db.get_snippet(name)
    if not snippet:
        console.print(f"[red]Snippet '{name}' not found.[/red]")
        raise SystemExit(1)
    syntax = Syntax(snippet.code, snippet.language or "text", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=f"{snippet.name} ({snippet.language or 'text'})"))


@cli.command()
@click.argument("name")
@click.option("--description", "-d", default=None, help="New description")
@click.option("--language", "-l", default=None, help="New language")
@click.option("--tags", "-t", default=None, help="New comma-separated tags")
@click.option("--code", "-c", default=None, help="New code (or use stdin)")
def edit(name, description, language, tags, code):
    """Edit an existing snippet."""
    snippet = db.get_snippet(name)
    if not snippet:
        console.print(f"[red]Snippet '{name}' not found.[/red]")
        raise SystemExit(1)
    if description is not None:
        snippet.description = description
    if language is not None:
        snippet.language = language
    if tags is not None:
        snippet.tags = [t.strip() for t in tags.split(",") if t.strip()]
    if code is not None:
        snippet.code = code
    elif not click.get_text_stream("stdin").isatty():
        snippet.code = click.get_text_stream("stdin").read()
    db.update_snippet(name, snippet)
    console.print(f"[green]✓[/green] Snippet '{name}' updated!")


@cli.command()
@click.argument("filepath", type=click.File("w"))
def export(filepath):
    """Export all snippets to a JSON file."""
    json_data = db.export_json()
    filepath.write(json_data)
    console.print(f"[green]✓[/green] Exported to {filepath.name}!")


@cli.command()
@click.argument("filepath", type=click.File("r"))
def import_(filepath):
    """import quicksnippets from a JSON file."""
    json_data = filepath.read()
    count = db.import_json(json_data)
    console.print(f"[green]✓[/green] Imported {count} snippets!")


@cli.command()
def stats():
    """Show snippet statistics."""
    snippets = db.list_snippets()
    if not snippets:
        console.print("[yellow]No snippets yet.[/yellow]")
        return
    languages: dict[str, int] = {}
    tags: dict[str, int] = {}
    for s in snippets:
        if s.language:
            languages[s.language] = languages.get(s.language, 0) + 1
        for tag in s.tags:
            tags[tag] = tags.get(tag, 0) + 1
    console.print(
        Panel.fit(
            f"[bold]Total Snippets:[/bold] {len(snippets)}\n"
            f"[bold]Languages:[/bold] {len(languages)}\n"
            f"[bold]Tags:[/bold] {len(tags)}",
            title="Statistics",
        )
    )
    if languages:
        console.print("\n[bold]Top Languages:[/bold]")
        for lang, count in sorted(languages.items(), key=lambda x: -x[1])[:5]:
            console.print(f"  {lang}: {count}")
    if tags:
        console.print("\n[bold]Top Tags:[/bold]")
        for tag, count in sorted(tags.items(), key=lambda x: -x[1])[:5]:
            console.print(f"  {tag}: {count}")


if __name__ == "__main__":
    cli()
