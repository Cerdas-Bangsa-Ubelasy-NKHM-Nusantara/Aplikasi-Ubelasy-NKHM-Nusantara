import React from 'react';

// Kelompokkan catatan berdasarkan bulan dan tahun (format "April 2025")
export const groupNotesByMonthYear = (notes) => {
  const groups = {};
  notes.forEach((note) => {
    const date = new Date(note.createdAt);
    const month = date.toLocaleString('id-ID', { month: 'long' });
    const year = date.getFullYear();
    const key = `${month} ${year}`;
    if (!groups[key]) groups[key] = [];
    groups[key].push(note);
  });

  // Urutkan grup dari terbaru ke terlama (descending)
  const sortedKeys = Object.keys(groups).sort((a, b) => {
    const dateA = new Date(a);
    const dateB = new Date(b);
    return dateB - dateA; // terbaru lebih dulu
  });

  const sortedGroups = {};
  sortedKeys.forEach((key) => {
    // Urutkan catatan di dalam grup dari terbaru ke terlama
    const sortedNotes = [...groups[key]].sort((a, b) => 
      new Date(b.createdAt) - new Date(a.createdAt)
    );
    sortedGroups[key] = sortedNotes;
  });
  return sortedGroups;
};

// Sorot kata kunci dalam teks (case-insensitive)
export const highlightText = (text, keyword) => {
  if (!keyword || keyword.trim() === '') return text;
  const regex = new RegExp(`(${keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  const parts = text.split(regex);
  return parts.map((part, i) =>
    regex.test(part) ? <mark key={i}>{part}</mark> : part
  );
};
