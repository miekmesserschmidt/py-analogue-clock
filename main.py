"""CLI for generating analogue clock SVGs."""

from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from analogue_clock import AnalogueClock

app = typer.Typer(help="Generate SVG analogue clock faces displaying specified times.")


@app.command()
def generate(
    svg_file: Path = typer.Argument(
        ...,
        help="Path to the input SVG file containing clock face with hour-hand, minute-hand, and optional second-hand elements.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    time: Optional[str] = typer.Option(
        None,
        "--time",
        "-t",
        help="Time to display in HH:MM:SS format. If not provided, uses current time.",
        metavar="HH:MM:SS",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path. If not provided, prints to stdout.",
        file_okay=True,
        dir_okay=False,
        writable=True,
    ),
    center: Optional[str] = typer.Option(
        None,
        "--center",
        "-c",
        help="Custom transform center as 'x,y' (e.g., '150,150'). If not provided, center is taken as the center of the svg",
        metavar="X,Y",
    ),
):
    """
    Generate an SVG clock face displaying the specified time.

    Examples:

        # Generate clock showing current time, output to stdout
        python main.py test_clock.svg

        # Generate clock showing specific time
        python main.py test_clock.svg --time 15:30:45

        # Save to file
        python main.py test_clock.svg --time 12:00:00 --output clock_noon.svg

        # Use custom transform center
        python main.py test_clock.svg --time 15:30:45 --center 100,100 --output clock.svg
    """
    try:
        # Load the input SVG
        with open(svg_file, "r") as f:
            svg_content = f.read()

        # Parse custom center if provided
        transform_center = None
        if center is not None:
            try:
                parts = center.split(",")
                if len(parts) != 2:
                    raise ValueError("Center must be in format 'x,y'")
                x, y = float(parts[0].strip()), float(parts[1].strip())
                transform_center = (x, y)
                typer.echo(f"Using custom transform center: ({x}, {y})", err=True)
            except ValueError as e:
                typer.echo(f"Error: Invalid center format - {e}", err=True)
                typer.echo("Center must be in format 'x,y' (e.g., '150,150')", err=True)
                raise typer.Exit(code=1)

        # Create clock instance (validates SVG)
        try:
            clock = AnalogueClock(svg=svg_content, transform_center=transform_center)
        except ValueError as e:
            typer.echo(f"Error: Invalid SVG - {e}", err=True)
            raise typer.Exit(code=1)

        # Determine the time to display
        if time is None:
            # Use current time
            now = datetime.now()
            display_time = now.strftime("%H:%M:%S")
            typer.echo(
                f"No time specified, using current time: {display_time}", err=True
            )
        else:
            display_time = time
            typer.echo(f"Generating clock for time: {display_time}", err=True)

        # Generate the clock SVG
        result_svg = clock.generate(display_time)

        # Output the result
        if output is None:
            # Print to stdout
            typer.echo(result_svg)
        else:
            # Write to file
            with open(output, "w") as f:
                f.write(result_svg)
            typer.echo(f"Clock SVG saved to: {output}", err=True)

    except FileNotFoundError as e:
        typer.echo(f"Error: File not found - {e}", err=True)
        raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo(f"Error: Invalid time format - {e}", err=True)
        typer.echo("Time must be in HH:MM:SS format (e.g., 14:30:45)", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
