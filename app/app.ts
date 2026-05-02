import express from "express";
import path from "path";
import { query } from "./db";

const app = express();
const port = process.env.PORT ? Number(process.env.PORT) : 8000;

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

app.get("/api/movies", async (req, res) => {
  try {
    const movies = await query("SELECT * FROM movie_diary ORDER BY date DESC LIMIT 100");
    res.json(movies);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Database error" });
  }
});

app.get("/api/tags", async (req, res) => {
  try {
    const tables = await query(`SHOW TABLES LIKE 'tag_%'`);
    const tableNames = tables.length
      ? tables.map((row: Record<string, any>) => {
          const name = String(Object.values(row)[0]);
          return name.startsWith("tag_") ? name.slice(4) : name;
        })
      : [];
    res.json(tableNames);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Database error" });
  }
});

app.get("/api/tags/:tags", async (req, res) => {
  const tagsParam = req.params.tags;
  const tags = tagsParam.split(':').filter(tag => tag.length > 0);

  if (tags.length === 0) {
    return res.status(400).json({ error: "No tags provided" });
  }

  try {
    if (tags.length === 1) {
      // Single tag case
      const movies = await query(
        `SELECT * FROM \`tag_${tags[0]}\``
      );
      res.json(movies);
    } else {
      // Multiple tags case - INNER JOIN all tag tables
      const tableNames = tags.map(tag => `\`tag_${tag}\``);
      const joinConditions = tags.slice(1).map((tag, index) => 
        `t${index}.film_title = t${index + 1}.film_title AND t${index}.film_year = t${index + 1}.film_year AND t${index}.date = t${index + 1}.date`
      ).join(' AND ');

      const queryStr = `
        SELECT t0.film_title, t0.film_year, t0.date
        FROM ${tableNames[0]} t0
        ${tableNames.slice(1).map((table, index) => `INNER JOIN ${table} t${index + 1} ON t0.film_title = t${index + 1}.film_title AND t0.film_year = t${index + 1}.film_year AND t0.date = t${index + 1}.date`).join(' ')}
      `;

      const movies = await query(queryStr);
      res.json(movies);
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Database error" });
  }
});

app.post("/api/diary", async (req, res) => {
  const { film_title, film_year, rating, liked, date } = req.body;
  try {
    await query(
      `INSERT INTO movie_diary (film_title, film_year, rating, liked, date) VALUES (?, ?, ?, ?, ?)`,
      [film_title, film_year, rating, liked, date]
    );
    res.status(201).json({ success: true });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Database error" });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});